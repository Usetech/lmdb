# coding=utf-8

import codecs
import csv
from optparse import make_option
from django.core.management import BaseCommand
import sys
from django.utils import timezone
from core.models import DistrictObject

__author__ = 'pparkhomenko'

class Command(BaseCommand):
    args = "<filename[. filename, filename...]>"
    help = "Imports csv file with districts to database"
    option_list = BaseCommand.option_list +\
                  (make_option("--encoding", dest="encoding", default="cp1251", help="File encoding"),)

    def handle(self, *args, **options):
        if len(args) == 0:
            sys.stderr.writelines("No files\n")
            return
        print options
        encoding = options['encoding']
        codecs.lookup(encoding)
        print "Importing districts"
        for filename in args:
            print "Importing districts from " + filename
            csvfile = open(filename, "rb")
            reader = csv.reader(csvfile, delimiter=';')
            self.import_data(reader, encoding)
            csvfile.close()

    def parse_header(self, header, encoding):
        id_index = -1
        name_index = -1
        index = 0
        for item in header:
            item = item.decode(encoding)
            print item
            if (item == u"Код"):
                id_index = index
            elif (item == u"Наименование"):
                name_index = index
            index = index + 1
        if id_index == -1 or name_index == -1:
            raise Exception("Invalid file headers")
        return id_index, name_index


    def import_data(self, reader, encoding):
        id_index, name_index = self.parse_header(reader.next(), encoding)
        for row in reader:
            id = row[id_index]
            name = row[name_index].decode(encoding)
            print id, name
            district = DistrictObject()
            district.id = id
            district.name = name
            district.created_at = timezone.localtime(timezone.now(), timezone.get_current_timezone())
            district.save()


