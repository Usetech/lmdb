# coding=utf-8
import codecs
import csv
from optparse import make_option
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
            sys.stderr.writelines("No files\n")
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
            index = index + 1
        if id == -1 or district_id == -1 or street_id == -1 or house == -1 or housing == -1 or building == -1:
            raise Exception("Invalid file headers")
        return id, district_id, street_id, house, housing, building


    def import_data(self, reader, encoding):
        _id, _district_id, _street_id, _house, _housing, _building = self.parse_header(reader.next(), encoding)
        for row in reader:
            id = int(row[_id])
            district_id = int(row[_district_id])
            street_id = int(row[_street_id])
            house = row[_house].decode(encoding)
            housing = row[_housing].decode(encoding)
            building = row[_building].decode(encoding)
            print id, district_id, street_id, house, housing, building
            district = DistrictObject.objects.get(pk=district_id)
            street = StreetObject.objects.get(pk=street_id)
            print district.name, street.name
            address = AddressObject();
            address.id = id
            address.district = district
            address.street = street
            address.house = house
            if len(housing) == 1 and housing.isalpha():
                address.house_letter = housing.upper()
                address.housing = ''
            else:
                address.house_letter = ''
                address.housing = housing
            address.building = building
            address.created_at = timezone.localtime(timezone.now(), timezone.get_current_timezone())
            address.save()


