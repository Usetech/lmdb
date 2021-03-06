# coding=utf-8

import codecs
import csv
from optparse import make_option
from django.core.management import BaseCommand
import sys
from django.utils import timezone
from core.models import StreetObject

__author__ = 'pparkhomenko'


class Command(BaseCommand):
    args = "<filename[. filename, filename...]>"
    help = "Imports csv file with streets to database"
    option_list = BaseCommand.option_list + \
                  (make_option("--encoding", dest="encoding", default="cp1251", help="File encoding"),)

    def handle(self, *args, **options):
        if len(args) == 0:
            sys.stderr.writelines("No files\n")
            return
        print options
        encoding = options['encoding']
        codecs.lookup(encoding)
        print "Importing streets"
        for filename in args:
            print "Importing streets from " + filename
            csvfile = open(filename, "rb")
            reader = csv.reader(csvfile, delimiter=';')
            self.import_data(reader, encoding)
            csvfile.close()

    def parse_header(self, header, encoding):
        id_index = -1
        name_index = -1
        type_index = -1
        iname_index = -1
        valid_index = -1
        index = 0
        for item in header:
            print item
            item = item.decode(encoding)
            print item
            if item == u"Уникальный код улицы":
                id_index = index
            elif item == u"Основное наименование (без типа топонима)":
                name_index = index
            elif item == u"Наименование типа топонима":
                type_index = index
            elif item == u"Наименование улицы для поиска, сортировки":
                iname_index = index
            elif item == u"Признак действующего наименования (1 — да, 0 — нет)":
                valid_index = index
            index += 1
        if id_index == -1 or name_index == -1 or type_index == -1 or iname_index == -1 or valid_index == -1:
            raise Exception("Invalid file headers")
        return id_index, name_index, type_index, iname_index, valid_index


    def import_data(self, reader, encoding):
        id_index, name_index, type_index, iname_index, valid_index = self.parse_header(reader.next(), encoding)
        print id_index, name_index, valid_index
        for row in reader:
            id = row[id_index].decode(encoding)
            name = row[name_index].decode(encoding)
            type = row[type_index].decode(encoding)
            iname = row[iname_index].decode(encoding)
            valid = int(row[valid_index])
            print id, name, valid

            updated_count = StreetObject.objects.filter(bti_id=id).update(
                name=name,
                type=type,
                iname=iname,
                valid=valid != 0,
                created_at=timezone.now()
            )
            if not updated_count:
                street = StreetObject()
                street.bti_id = id
                street.name = name
                street.type = type
                street.iname = iname
                street.valid = valid != 0
                street.created_at = timezone.now()
                street.save()