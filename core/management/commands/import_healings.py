# -*- coding: utf-8 -*-
# coding=utf-8

import codecs
import csv
from optparse import make_option
from sys import stderr
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
import sys
from core.models import HealthObjectType, StreetObject, AddressObject


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
            print u"Unknown address: " + streets[0].name + u", house '" + house + u"', letter '" + house_letter + u"', housing '" + housing + u"', building '" + building + "'\n"
            return None
        elif len(addresses) == 1:
            return addresses[0]
        address = None
        counter = 0
        for a in addresses:
            if a.street.valid:
                address = a
                counter += 1
        if (counter == 1):
            return address
        if address == None:
            stderr.write(u"Multiple invalid addresses at %d\n" % (number,))
        else:
            stderr.write(u"Multiple valid addresses at %d\n" % (number,))
        return None

    def get_addresses(self, streets, house, house_letter, housing, building):
        return AddressObject.objects.all().filter(street__in=streets).filter(house=house).filter(house_letter=house_letter).filter(housing=housing).filter(building=building)

    def import_data(self, reader, encoding):
        reader.next()
        header = self.parse_header(reader.next(), encoding)

        counter = 0
        updated = 0
        created = 0
        created_types = 0
        empty_types = 0
        empty_streets = 0
        unknown_streets = 0
        unknown_addresses = 0
        for row in reader:
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
                    print u"Unknown street: " + street
                    unknown_streets += 1
                    unknown_addresses += 1
                else:
                    address = self.get_address(header, row, streets, encoding, counter + 3)
                    if (address == None):
                        unknown_addresses += 1

            counter += 1
            if counter % 100 == 0:
                print "Updated: %d; Created: %d" % (updated, created)

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


