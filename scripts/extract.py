import csv
import datetime
import urllib
import os

from dataconverters import xls
from os.path import join

CACHE_PATH = join('..', 'archive', 'shiller.xls')

OUT_FILEPATH = join('..', 'data', 'data.csv')

def extract(fp=CACHE_PATH):
    rows, metadata = xls.parse(open(fp))
    # convert from iterator to list and rows of dictionaries to rows of lists
    rows = [ [row[f['id']] for f in metadata['fields']] for row in rows ]

    # headings spread across rows 2-8
    header = [
        'Date',
        'SP500',
        'Dividend',
        'Earnings',
        'Consumer Price Index',
        'Long Interest Rate',
        'Real Price',
        'Real Dividend',
        'Real Earnings',
        'PE10'
        ]

    # first rows is header, last row is footnotes
    data = filter(is_valid_raw, rows)
    transposed = zip(*data)
    # remove empty column in the end
    del transposed[11]
    # fix dates
    # delete "date fraction" column
    del transposed[5]
    # seem to have a random extra blank 6 columns
    del transposed[-6:]
    transposed[0] = [ _fixdates(val) for val in transposed[0] ]
    for idx, row in enumerate(transposed[1:]):
        row = [ _fixup(val) for val in row ]
        transposed[idx+1] = row
    
    data = zip(*transposed)
    fout = open(OUT_FILEPATH, 'w')
    writer = csv.writer(fout, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(data)

def is_valid_raw(raw):
    return isinstance(raw[0], float)
	
def _fixup(val):
    if val == 'NA':
        return ''
    elif val == '':
        return ''
    try:
        return round(val, 2)
    except:
        print 'Unable to convert to float: %s' % val
        return ''

def _fixdates(val):
    # 1879.03 = march, 1879.1 = october
    val = round(val,2)
    year = int(val)
    # add 0.0001 to ensure we don't have problems re rounding
    month = int(0.1 + (val - year) * 100)
    out = str(year) + '-' + str(month).zfill(2) + '-01'
    return out	
	
if __name__ == '__main__':
    extract()
