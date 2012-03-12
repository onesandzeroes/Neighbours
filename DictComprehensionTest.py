#! /usr/bin/env python3
import csv

f1 = open('SUBTLEXonlyfrequency.csv', 'r')
inputFile = csv.reader(f1, dialect='excel')

freqDict = {line[0][0].lower(): {line[0]: line[1]} for line in inputFile}

