#!/usr/bin/env python
# -*- coding: utf-8 -*-import os
# 2019 - Bruno Adelé <brunoadele@gmail.com>

# https://www.lesechosdechaluguiville.com/app/download/12900843327/DT3386.pdf?t=1494447416&mobile=1
# https://www.sferiel.com/client/document/nt2005-0666-mode-d-emploi-compteur-phoenix_28.pdf
# https://www.sferiel.com/client/document/notice-delta_3.pdf

from datetime import datetime
from datetime import timedelta
import sys

if len(sys.argv) != 3:
    print("Usage: {sys.argv[0]} <INPUT> <OUTPUT>")
    sys.exit(1)

INPUT=sys.argv[1]
OUTPUT=sys.argv[2]

# Read file
with open(INPUT, 'r') as ifile:
    content = ifile.read()
    lines = content.split('\n')

# Show summaries
csv = []
sample = {}
getspeedcolumns = False
speeds = []
for line in lines:
    columns = line.split('.')
    columns = [int(i) for i in columns[:-1]]
    size = len(columns)

    # Get metadata
    if size>12:
        counterid = columns[0]
        department = columns[1]
        section = columns[2]
        indice = columns[3]
        direction = columns[4]
        year = columns[5]
        month = columns[6]
        day = columns[7]
        hour = columns[8]
        minute = columns[9]
        interval = columns[10]
        mode = columns[11]
        sampletype = columns[12]

        print(f"N° compteur({counterid:4d}) Department({department:4d}) Section({section:4d}) Indice({indice:4d}) \
Direction({direction:4d}) Year({year:4d}) Month({month:4d}) Day({day:4d}) Hour: {hour:4d}) Min: {minute:4d}) \
Intervale:( {interval:4d}) Mode: {mode:4d}) Type: {sampletype:4d})")

        str_time = f'20{year:02d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:00.0'
        current_date = datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S.%f')
        getspeedcolumns = True
    else:
        if getspeedcolumns:
            speeds = columns
            getspeedcolumns = False
        else:
            current_date = current_date + timedelta(minutes=interval)
            timestamp = int(datetime.timestamp(current_date))
            cyear = current_date.timetuple().tm_year
            cmonth = current_date.timetuple().tm_mon
            cday = current_date.timetuple().tm_mday
            chour = current_date.timetuple().tm_hour
            cmin = current_date.timetuple().tm_min


            for idx in range(len(columns)):
                if columns[idx] > 0:
                    csv.append(f'{counterid},{department},{section},{indice},{direction},{timestamp},{cyear},{cmonth},{cday},{chour},{cmin:02d},{speeds[idx]},{columns[idx]}')

# Write file
with open(OUTPUT, 'w') as ofile:
    ofile.write("counterid,department,section,indice,direction,timestamp,year,month,day,hour,min,speed,value\n")
    for line in csv:
        ofile.write(f"{line}\n")
