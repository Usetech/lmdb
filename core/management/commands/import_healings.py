# coding=utf-8

import codecs
import csv
from optparse import make_option
from sys import stderr
from django.core.management import BaseCommand
from core.models import HealthObjectType, StreetObject, AddressObject, LegalEntity, HealingObject


__author__ = 'pparkhomenko'

class Command(BaseCommand):
    args = "<filename>"
    help = "Imports csv file with healings to database"
    option_list = BaseCommand.option_list +\
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
            parsed[key] =  index
            print "# " + str(index) + " : " + key
            index += 1
        print parsed
        return parsed

    def get_address(self, header, row, streets, encoding, number):
        house = row[header["ADRES_DOM"]].decode(encoding)
        house_letter = row[header["ADRES_DOM_litera"]].decode(encoding).upper()
        housing = row[header["ADRES_KORPUS"]].decode(encoding)
        building = row[header["ADRES_STROENIE"]].decode(encoding)

        addresses = self.get_addresses(streets, house, house_letter, housing, building)
        if len(addresses) == 0 and len(housing) > 0:
            addresses = self.get_addresses(streets, house + '/' + housing, house_letter, '', building)
        if len(addresses) == 0 and (len(housing) > 0 or (len(building) > 0)):
            addresses = self.get_addresses(streets, house, house_letter, building, housing)
        if len(addresses) == 0 and len(house_letter):
            addresses = self.get_addresses(streets, house + house_letter, '', building, housing)

        if len(addresses) == 0:
            stderr.write(u"Unknown address at %d\n" % (number,))
            error = u"Unknown address: " + streets[0].name + u", дом '" + house + u"', литера '" + house_letter + u"', корпус '" + housing + u"', строение '" + building + "'\n"
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
            error = u"Множество недействующих адресов"
        else:
            stderr.write(u"Multiple valid addresses at %d\n" % (number,))
            error = u"Множество действующих адресов"
        return None, error


    def get_addresses(self, streets, house, house_letter, housing, building):
        return AddressObject.objects.all().filter(street__in=streets).filter(house=house).filter(house_letter=house_letter).filter(housing=housing).filter(building=building)


    def fill_chief_data(self, header, row, data, number, encoding):
        data.chief_original_name = row[header["RUKOVODIT"]].decode(encoding)
        sex = str(row[header["R_POL"]].decode(encoding)).lower()
        if sex == u"муж" or sex == u"м":
            data.chief_sex = 'M'
        elif sex == u"жен" or sex == u"ж":
            data.chief_sex = 'F'
        else:
            if len(sex) > 0:
                stderr.write(u"Unknown sex at " + str(number))
            data.chief_sex = None
        data.chief_phone = row[header["R_TEL_NOMER"]].decode(encoding)


    def import_le_data(self, reader, encoding):
        reader.next()
        header = self.parse_header(reader.next(), encoding)

        counter = 0
        empty_streets = 0
        unknown_streets = 0
        unknown_addresses = 0
        legal_entities = {}
        for row in reader:
            print "Processing line %d" % counter
            counter += 1
            lpu = row[header["GLAVNOE_LPU"]].decode(encoding)
            if len(lpu) == 0:
                lpu = row[header["NAME"]].decode(encoding)
            elif legal_entities.has_key(lpu):
                continue

            street = row[header["ADRES_UL_NAME"]].decode(encoding)
            address = None
            if len(street) == 0:
                # stderr.write(u"Empty street at %d\n" % (counter + 3,))
                empty_streets += 1
                unknown_addresses += 1
            else:
                streets = StreetObject.objects.all().filter(name=street)
                if len(streets) == 0:
                    # stderr.write(u"Unknown street at %d\n" % (counter + 3,))
                    error = u"Улица не найдена: " + street
                    unknown_streets += 1
                    unknown_addresses += 1
                else:
                    address, error = self.get_address(header, row, streets, encoding, counter + 3)
                    if (address == None):
                        unknown_addresses += 1

            le = LegalEntity()
            le.name = lpu
            self.fill_chief_data(header, row, le, counter + 3, encoding)
            le.fact_address = address
            le.original_address = row[header["ADRES_STR"]].decode(encoding)
            le.errors = error
            le.save()
            legal_entities[lpu] = le

        print "Total: %d" % (counter,)
        print "Unknown addresses: %d" % (unknown_addresses,)
        print "Empty streets: %d" % (empty_streets,)
        print "Unknown streets: %d" % (unknown_streets,)



    def import_mu_data(self, legal_entities, reader, encoding):
        reader.next()
        header = self.parse_header(reader.next(), encoding)

        counter = 0
        created_types = 0
        empty_types = 0
        empty_streets = 0
        unknown_streets = 0
        unknown_addresses = 0
        for row in reader:
            lpu = row[header["GLAVNOE_LPU"]].decode(encoding)
            if len(lpu) == 0:
                lpu = row[header["NAME"]].decode(encoding)
            lpu = legal_entities[lpu]
            hotype = row[header["TYPE"]].decode(encoding)
            if len(hotype) == 0:
                stderr.write(u"Empty type at %d\n" % (str(counter + 3),))
                empty_types += 1
                continue
            hotype, created = HealthObjectType.objects.get_or_create(name=hotype)
            if (created):
                created_types += 1

            street = row[header["ADRES_UL_NAME"]].decode(encoding)
            address = None
            if len(street) == 0:
                stderr.write(u"Empty street at %d\n" % (counter + 3,))
                empty_streets += 1
                unknown_addresses += 1
            else:
                streets = StreetObject.objects.all().filter(name=street)
                if len(streets) == 0:
                    stderr.write(u"Unknown street at %d\n" % (counter + 3,))
                    error = u"Улица не найдена: " + street
                    unknown_streets += 1
                    unknown_addresses += 1
                else:
                    address, error = self.get_address(header, row, streets, encoding, counter + 3)
                    if (address == None):
                        unknown_addresses += 1

            mu = HealingObject()
            mu.object_type = hotype
            mu.legal_entity = lpu
            self.fill_chief_data(header, row, mu, counter + 3, encoding)
            mu.address = address
            mu.original_address = row[header["ADRES_STR"]].decode(encoding)
            mu.name = row[header["NAME"]].decode(encoding)
            mu.short_name = row[header["SHORT_NAME"]].decode(encoding)
            mu.full_name = row[header["FULL_NAME"]].decode(encoding)
            mu.global_id = row[header["GLOBALID"]]
            mu.info = row[header["INFO"]].decode(encoding)
            mu.errors = error
            mu.save()

            counter += 1

        print "Total: %d" % (counter,)
        print "Unknown addresses: %d" % (unknown_addresses,)
        print "Empty streets: %d" % (empty_streets,)
        print "Unknown streets: %d" % (unknown_streets,)
        print "Empty types: %d" % (empty_types,)





        #     district_id = int(row[_district_id])
        #     street_id = int(row[_street_id])
        #     house_letter = None
        #     house = row[_house].decode(encoding)
        #     housing = row[_housing].decode(encoding)
        #     building = row[_building].decode(encoding)
        #
        #     if len(housing) == 1 and housing.isalpha():
        #         house_letter = housing.upper()
        #         housing = ''
        #     else:
        #         house_letter = ''
        #
        #     address, new_created = AddressObject.objects.get_or_create(
        #         bsi_id=id,
        #         defaults={
        #             'house': house,
        #             'house_letter': house_letter,
        #             'housing': housing,
        #             'building': building,
        #             'street_id': street_id,
        #             'district_id': district_id,
        #             'created_at': timezone.now()
        #         }
        #     )
        #     if new_created:
        #         created += 1
        #     else:
        #         updated += 1


