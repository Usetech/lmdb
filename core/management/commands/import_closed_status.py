# coding=utf-8

import codecs
import csv
import json
from optparse import make_option
import re
from sys import stderr
import datetime
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from core.models import HealingObject, HealthObjectType, ClosingReason


__author__ = 'pparkhomenko'


class Command(BaseCommand):
    args = "<filename>"
    help = "Imports csv file with healing objects to database"
    option_list = BaseCommand.option_list + make_option("--encoding",
                                                        dest="encoding", default="cp1251", help="File encoding"),

    def handle(self, *args, **options):
        if len(args) == 0:
            stderr.writelines("No files\n")
            return
        print options
        encoding = options['encoding']
        codecs.lookup(encoding)
        filename = args[0]
        print "Importing healings from " + filename
        csv_file = open(filename, "rb")
        reader = csv.reader(csv_file, delimiter=';')
        self.import_mu_data(reader, encoding)
        csv_file.close()

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

    def getHealingObject(self, header, row, name, encoding, number):
        ho_type = row[header["TYPE"]].decode(encoding).strip()
        ho_type = HealthObjectType.objects.get(name=ho_type)
        address = row[header["ADRES_STR"]].decode(encoding).strip()
        rs = HealingObject.objects.all(). \
            filter(object_type=ho_type). \
            filter(name=name). \
            filter(original_address=address)
        if len(rs) > 1:
            stderr.write("Too many healing objects at %d\n" % (number,))
            return None
        if len(rs) < 1:
            stderr.write("Healing object not found at %d\n" % (number,))
            return None
        return rs[0]

    date_re = re.compile(r'^(\d{2})\.(\d{2})\.(\d{4})[^\d]*$')

    def parse_date(self, date_string):
        if (len(date_string) == 0) or (date_string == "-"):
            return None
        parts = self.date_re.match(date_string)
        if parts is None:
            stderr.write("Invalid date: %s\n" % (date_string,))
            return None
        day, month, year = parts.group(1, 2, 3)
        date = datetime.date(int(year), int(month), int(day))
        return date

    def import_mu_data(self, reader, encoding):
        reader.next()
        header = self.parse_header(reader.next(), encoding)

        counter = 2
        errors = 0
        for row in reader:
            print "Processing row", counter
            counter += 1
            name = row[header["NAME"]].decode(encoding).strip()
            if len(name) == 0:
                stderr.write("Healing object name is empty at %d\n" % counter)
                continue

            is_closed = row[header["PRIZNAK_CLOSE"]].decode(encoding).strip().lower() == 'true'

            mu = self.getHealingObject(header, row, name, encoding, counter)
            if not (mu is None):
                mu.is_closed = is_closed
                mu.closing_reason = self.get_closing_reason(row[header["Prichina_CLOSE"]].decode(encoding).strip())
                mu.closed_at = self.parse_date(row[header["DATA_CLOSE"]].decode(encoding).strip())
                mu.opened_at = self.parse_date(row[header["DATA_REOPEN"]].decode(encoding).strip())
                try:
                    mu.clean_fields()
                    mu.save()
                except ValidationError as e:
                    self.show_validation_error("Error validating healing object", mu, e)
                    raise
                pass
            else:
                errors += 1

        print "Total: %d" % (counter,)
        print "Invalid healing objects: %d" % (errors,)

    def show_validation_error(self, message, object, e):
        print message
        print serializers.serialize('json', [object])
        print json.dumps(e.message_dict)

    def get_closing_reason(self, reason_name):
        reason = ClosingReason.objects.get_or_create(name=reason_name)
        return reason

