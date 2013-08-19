# coding=utf-8
import codecs
import csv
from optparse import make_option
from sys import stderr
from django.core.management import BaseCommand


__author__ = 'pparkhomenko'

class Command(BaseCommand):
    args = "<filename[. filename, filename...]>"
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
        print "Importing healings"
        for filename in args:
            print "Importing healings from " + filename
            csvfile = open(filename, "rb")
            reader = csv.reader(csvfile, delimiter=';')
            self.import_data(reader, encoding)
            csvfile.close()


    def parse_header(self, header, encoding):
        parsed = {}
        index = 0
        for item in header:
            key = item.decode(encoding)
            if parsed.has_key(key):
                raise Exception("Duplicate key in header: " + key)
            parsed[str(item)] =  index
            index += 1
        print parsed
        return parsed

    def import_data(self, reader, encoding):
        reader.next()
        header = self.parse_header(reader.next(), encoding)

        # counter = 0
        # updated = 0
        # created = 0
        # for row in reader:
        #     print row
        #
        #     id = int(row[_id])
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
        #
        #     counter += 1
        #     if counter % 100 == 0:
        #         print "Updated: %d; Created: %d" % (updated, created)

