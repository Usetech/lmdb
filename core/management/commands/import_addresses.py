# coding=utf-8
import codecs
import csv
from optparse import make_option
from sys import stderr
from django.core.management import BaseCommand
from django.utils import timezone
from core.models import StreetObject, DistrictObject, AddressObject


__author__ = 'pparkhomenko'


class Command(BaseCommand):
    args = "<filename[. filename, filename...]>"
    help = "Imports csv file with addresses to database"
    option_list = BaseCommand.option_list +\
                  (make_option("--encoding", dest="encoding", default="cp1251", help="File encoding"),)

    def handle(self, *args, **options):
        if len(args) == 0:
            stderr.writelines("No files\n")
            return
        print options
        encoding = options['encoding']
        codecs.lookup(encoding)
        print "Importing addresses"
        for filename in args:
            print "Importing addresses from " + filename
            csvfile = open(filename, "rb")
            reader = csv.reader(csvfile, delimiter=';')
            self.import_data(reader, encoding)
            csvfile.close()

    def parse_header(self, header, encoding):
        id = -1
        district_id = -1
        street_id = -1
        house = -1
        housing = -1
        building = -1

        index = 0
        for item in header:
            item = item.decode(encoding)
            print item
            if item == u"Уникальный идентификатор записи каталога":
                id = index
            elif item == u"Код административного округа":
                district_id = index
            elif item == u"Код улицы":
                street_id = index
            elif item == u"Дом номер":
                house = index
            elif item == u"Корпус номер":
                housing = index
            elif item == u"Строение номер":
                building = index
            index += 1
        if id == -1 or district_id == -1 or street_id == -1 or house == -1 or housing == -1 or building == -1:
            raise Exception("Invalid file headers")
        return id, district_id, street_id, house, housing, building

    def import_data(self, reader, encoding):
        _id, _district_id, _street_id, _house, _housing, _building = self.parse_header(reader.next(), encoding)
        counter = 0
        updated = 0
        created = 0
        for row in reader:
            id = row[_id].decode(encoding)
            district_id = int(row[_district_id])
            street_id = row[_street_id]
            house = row[_house].decode(encoding)
            housing = row[_housing].decode(encoding)
            building = row[_building].decode(encoding)

            streets = StreetObject.objects.all().filter(bti_id=street_id)
            if len(streets) != 1:
                raise Exception("More then one street found for id " + street_id + " at " + str(counter))
            street = streets[0]

            address = AddressObject()
            address.bti_id = id
            address.district_id = district_id
            address.street = street
            address.house = house
            if len(housing) == 1 and housing.isalpha():
                address.house_letter = housing.upper()
                address.housing = u""
            else:
                address.house_letter = u""
                address.housing = housing
            address.building = building
            address.full_address_string = address.full_string()

            record_updated = AddressObject.objects.filter(bti_id=id).update(
                district=address.district_id,
                street=street.id,
                house=address.house,
                house_letter=address.house_letter,
                housing=address.housing,
                building=address.building,
                full_address_string=address.full_string()
            )

            if not record_updated:
                created += 1
                address.save()
            else:
                updated += 1

            counter += 1
            if counter % 500 == 0:
                print "Updated: %d; Created: %d" % (updated, created)


