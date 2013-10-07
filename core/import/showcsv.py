#!/usr/bin/python

import codecs
import csv
import os
import sys


def main(path):
    path = os.path.abspath(path)
    for filename in os.listdir(path):
        filename = os.path.join(path, filename)
        if os.path.isfile(filename):
            undef, ext = os.path.splitext(filename)
            ext = ext.lower()
            if ext == ".csv":
                file = open(filename, "rb")
                reader = csv.reader(file, delimiter=';')
                parsecsv(reader)


def parsecsv(reader):
    #reader.next()
    for row in reader:
        for item in row:
            item = item.decode("cp1251")
        print row




main(sys.argv[1])


