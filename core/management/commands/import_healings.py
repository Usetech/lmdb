# coding=utf-8

import codecs
import csv
import json
from optparse import make_option
from sys import stderr
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from core.management.commands.mappings import object_type_to_service_type
from core.models import HealthObjectType, StreetObject, AddressObject, LegalEntity, HealingObject, Service, ServiceType


__author__ = 'pparkhomenko'


class Command(BaseCommand):
    args = "<filename>"
    help = "Imports csv file with healings to database"
    option_list = BaseCommand.option_list + \
                  (make_option("--encoding", dest="encoding", default="cp1251", help="File encoding"),)

    def handle(self, *args, **options):
        if len(args) == 0:
            stderr.writelines("No files\n")
            return
        print options
        encoding = options['encoding']
        codecs.lookup(encoding)
        filename = args[0]
        print "Importing healings from " + filename
        csvfile = open(filename, "rb")
        reader = csv.reader(csvfile, delimiter=';')
        print "Importing Legal Entities..."
        lemap = self.import_le_data(reader, encoding)
        csvfile.close()
        csvfile = open(filename, "rb")
        print "Importing Healings..."
        reader = csv.reader(csvfile, delimiter=';')
        self.import_mu_data(lemap, reader, encoding)
        csvfile.close()

    def parse_header(self, header, encoding):
        parsed = {}
        index = 0
        for item in header:
            key = item.decode(encoding)
            if parsed.has_key(key):
                raise Exception("Duplicate key in header: " + key)
            parsed[key] = index
            print "# " + str(index) + " : " + key
            index += 1
        print parsed
        return parsed

    def get_full_city_name(self, city, type):
        if type is None or len(type) == 0:
            return u"город " + city
        return type + u" " + city


    def is_default_city(self, city, type):
        if city is None or len(city) == 0:
            return True
        return self.get_full_city_name(city, type).lower() in {u"город москва", u"город зеленоград"};


    def get_streets(self, header, row, street, encoding):
        city = row[header["ADRES_NASELENPUNKT"]].decode(encoding).strip()
        city_type = row[header["NASELEN_PUNKT"]].decode(encoding).lower().strip()
        street_type = row[header["ADRES_UL_TYPE"]].decode(encoding).lower().strip()
        if self.is_default_city(city, city_type):
            return StreetObject.objects.all().filter(name=street)
        iname = street + " " + street_type + " (" + self.get_full_city_name(city, city_type) + ")"
        streets = StreetObject.objects.all().filter(iname=iname)
        if len(streets):
            return streets
        so = StreetObject()
        so.name = street
        so.type = street_type
        so.iname = iname
        so.save()
        return [so,]

    def get_address(self, header, row, streets, encoding, number):
        city = row[header["ADRES_NASELENPUNKT"]].decode(encoding).strip()
        city_type = row[header["NASELEN_PUNKT"]].decode(encoding).lower().strip()
        house = row[header["ADRES_DOM"]].decode(encoding).upper().strip()
        house_letter = row[header["ADRES_DOM_litera"]].decode(encoding).upper().strip()
        housing = row[header["ADRES_KORPUS"]].decode(encoding).strip()
        building = row[header["ADRES_STROENIE"]].decode(encoding).strip()

        addresses = self.get_addresses(city, city_type, streets, house, house_letter, housing, building)
        if len(addresses) == 0 and len(housing) > 0:
            addresses = self.get_addresses(city, city_type, streets, house + '/' + housing, house_letter, '', building)
        if len(addresses) == 0 and (len(housing) > 0 or (len(building) > 0)):
            addresses = self.get_addresses(city, city_type, streets, house, house_letter, building, housing)
        if len(addresses) == 0 and len(house_letter):
            addresses = self.get_addresses(city, city_type, streets, house + house_letter, '', building, housing)

        if len(addresses) == 0 and not self.is_default_city(city, city_type):
            zip_code = row[header["ADRES_INDEX"]].decode(encoding).strip()
            if len(zip_code) > 6:
                return None, u"Ошибка в индексе: " + zip_code
            address = AddressObject()
            address.city = city
            address.city_type = city_type
            address.street = streets[0]
            address.house = house
            address.house_letter = house_letter
            address.housing = housing
            address.building = building
            address.zip_code = zip_code
            address.area = row[header["ADRES_OBL"]].decode(encoding).strip()
            address.full_address_string = address.full_string()
            address.save()
            return address, u"Новый адрес"

        address_string = streets[0].name + u", дом '" + house + u"', литера '" + house_letter + u"', корпус '" +\
                         housing + u"', строение '" + building + "'"

        if len(addresses) == 0:
            stderr.write(u"Unknown address at %d\n" % (number,))
            error = u"Неизвестный адрес: " + address_string
            return None, error
        elif len(addresses) == 1:
            return addresses[0], None
        address = None
        counter = 0
        for a in addresses:
            if a.street.valid:
                address = a
                counter += 1
        if (counter == 1):
            return address, None
        if address == None:
            stderr.write(u"Multiple invalid addresses at %d\n" % (number,))
            error = u"Множество недействующих адресов для " + address_string
        else:
            stderr.write(u"Multiple valid addresses at %d\n" % (number,))
            error = u"Множество действующих адресов для " + address_string
        return None, error


    def get_addresses(self, city, city_type, streets, house, house_letter, housing, building):
        rs = AddressObject.objects.all().filter(street__in=streets).filter(house=house).filter(
                house_letter=house_letter).filter(housing=housing).filter(building=building)
        if self.is_default_city(city, city_type):
            return rs
        rs.filter(city=city).filter(city_type=city_type)
        return rs


    def fill_chief_data(self, header, row, data, number, encoding):
        data.chief_original_name = row[header["RUKOVODIT"]].decode(encoding).strip()
        sex = row[header["R_POL"]].decode(encoding).lower().strip()
        if sex == u"муж" or sex == u"м":
            data.chief_sex = 'M'
        elif sex == u"жен" or sex == u"ж":
            data.chief_sex = 'F'
        else:
            if len(sex) > 0:
                stderr.write(u"Unknown sex at " + str(number))
            data.chief_sex = None
        data.chief_phone = row[header["R_TEL_NOMER"]].decode(encoding).strip()


    def import_le_data(self, reader, encoding):
        reader.next()
        header = self.parse_header(reader.next(), encoding)

        counter = 2
        empty_streets = 0
        unknown_streets = 0
        unknown_addresses = 0
        legal_entities = {}
        for row in reader:
            print "Processing row", counter
            counter += 1

            lpu = row[header["GLAVNOE_LPU"]].decode(encoding).strip()
            if len(lpu) == 0:
                lpu = row[header["NAME"]].decode(encoding).strip()
            if len(lpu) == 0:
                stderr.write("Legal entity name is empty at %d\n" % (counter))
                continue
            if legal_entities.has_key(lpu):
                continue

            street = row[header["ADRES_UL_NAME"]].decode(encoding).strip()
            address = None
            error = None
            if len(street) == 0:
                # stderr.write(u"Empty street at %d\n" % (counter,))
                empty_streets += 1
                unknown_addresses += 1
            else:
                streets = self.get_streets(header, row, street, encoding)
                if len(streets) == 0:
                    # stderr.write(u"Unknown street at %d\n" % (counter,))
                    error = u"Улица не найдена: " + street
                    unknown_streets += 1
                    unknown_addresses += 1
                else:
                    address, error = self.get_address(header, row, streets, encoding, counter)
                    if not address:
                        unknown_addresses += 1

            le = LegalEntity()
            le.name = lpu
            le.original_name = row[header["NAME"]].decode(encoding).strip()
            self.fill_chief_data(header, row, le, counter, encoding)
            le.fact_address = address
            le.original_address = row[header["ADRES_STR"]].decode(encoding).strip()
            le.errors = error
            try:
                le.clean_fields()
                le.save()
            except ValidationError as e:
                self.show_validation_error("Error validating legal entity object", le, e)
                raise

            legal_entities[lpu] = le

        print "Total: %d" % (counter - 2,)
        print "Unknown addresses: %d" % (unknown_addresses,)
        print "Empty streets: %d" % (empty_streets,)
        print "Unknown streets: %d" % (unknown_streets,)

        return legal_entities

    def import_mu_data(self, legal_entities, reader, encoding):
        reader.next()
        header = self.parse_header(reader.next(), encoding)

        counter = 2
        created_types = 0
        empty_types = 0
        empty_streets = 0
        unknown_streets = 0
        unknown_addresses = 0
        for row in reader:
            print "Processing row", counter
            counter += 1
            lpu = row[header["GLAVNOE_LPU"]].decode(encoding).strip()
            if len(lpu) == 0:
                lpu = row[header["NAME"]].decode(encoding).strip()
            if len(lpu) == 0:
                stderr.write("Legal entity name is empty at %d" % (counter))
                continue
            lpu = legal_entities[lpu]
            hotype = row[header["TYPE"]].decode(encoding).strip()
            if len(hotype) == 0:
                stderr.write(u"Empty type at %d\n" % (str(counter + 3),))
                empty_types += 1
                continue
            hotype, created = HealthObjectType.objects.get_or_create(name=hotype)
            if created:
                created_types += 1

            street = row[header["ADRES_UL_NAME"]].decode(encoding).strip()
            address = None
            if len(street) == 0:
                stderr.write(u"Empty street at %d\n" % (counter + 3,))
                empty_streets += 1
                unknown_addresses += 1
            else:
                streets = self.get_streets(header, row, street, encoding)
                if len(streets) == 0:
                    stderr.write(u"Unknown street at %d\n" % (counter + 3,))
                    error = u"Улица не найдена: " + street
                    unknown_streets += 1
                    unknown_addresses += 1
                else:
                    address, error = self.get_address(header, row, streets, encoding, counter + 3)
                    if address is None:
                        unknown_addresses += 1

            mu = HealingObject()
            mu.object_type = hotype
            mu.legal_entity = lpu
            #self.fill_chief_data(header, row, mu, counter + 3, encoding)
            mu.address = address
            mu.original_address = row[header["ADRES_STR"]].decode(encoding).strip()
            name = row[header["NAME"]].decode(encoding).strip()
            mu.name = name
            mu.short_name = row[header["SHORT_NAME"]].decode(encoding).strip()
            mu.full_name = row[header["FULL_NAME"]].decode(encoding).strip() or name
            mu.global_id = row[header["GLOBALID"]].strip()
            mu.info = row[header["INFO"]].decode(encoding).strip()
            mu.errors = error
            try:
                mu.clean_fields()
                mu.save()
            except ValidationError as e:
                self.show_validation_error("Error validating healing object", mu, e)
                raise

            service = Service()
            service.healing_object = mu
            service_type_name = object_type_to_service_type[hotype.name]
            service.service = ServiceType.objects.get(name=service_type_name)
            self.fill_chief_data(header, row, service, counter + 3, encoding)
            service.phone = row[header["TEL_NOMER"]].decode(encoding).strip()
            service.fax = row[header["FAX_NOMER"]].decode(encoding).strip()
            service.info = row[header["INFO"]].decode(encoding).strip()
            # service.workdays = row[header["DNY_RABOTY1"]].decode(encoding).strip()
            # service.workhours = row[header["CHAS_RABOTY"]].decode(encoding).strip()
            # service.daysoff = row[header["DNY_NE_RABOT"]].decode(encoding).strip()
            # service.daysoff_restrictions = row[header["VYHODNOJ_TYPE"]].decode(encoding).strip()
            service.specialization = row[header["SPECIAL"]].decode(encoding).strip()
            service.paid_services = row[header["PLAT_USLUGI"]].decode(encoding).strip()
            service.free_services = row[header["BESPL_USLUGI"]].decode(encoding).strip()
            service.drug_provisioning = row[header["LEK_OBESP"]].decode(encoding).strip()
            service.departments = row[header["OTDELENIE"]].decode(encoding).strip()
            service.hospital_levels = row[header["LVL"]].decode(encoding).strip()
            service.tour = row[header["SMENA"]].decode(encoding).strip()
            service.receipes_provisioning = row[header["RECEPT"]].decode(encoding).strip()
            service.drugstore_type = row[header["DRUGSTORE_TYPE"]].decode(encoding).strip()
            service.hospital_type = row[header["HOSPITAL_TYPE"]].decode(encoding).strip()
            beds = row[header["KOIKI"]].decode(encoding).strip()
            if len(beds) == 0:
                beds = row[header["KOJKA"]].decode(encoding).strip()
                if len(beds) == 0:
                    beds = row[header["KOIKA"]].decode(encoding).strip()
            service.hospital_beds = beds
            try:
                service.clean_fields()
                service.save()
            except ValidationError as e:
                self.show_validation_error("Error validating service", service, e)
                raise

        print "Total: %d" % (counter,)
        print "Unknown addresses: %d" % (unknown_addresses,)
        print "Empty streets: %d" % (empty_streets,)
        print "Unknown streets: %d" % (unknown_streets,)
        print "Empty types: %d" % (empty_types,)


    def show_validation_error(self, message, object, e):
        print message
        print serializers.serialize('json', [object])
        print json.dumps(e.message_dict)


