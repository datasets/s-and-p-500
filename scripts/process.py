import csv
import datetime
import urllib
import os

from dataconverters import xls

url = 'http://www.econ.yale.edu/~shiller/data/ie_data.xls'
cachepath = 'archive/shiller.xls'

out_filepath = 'data/data.csv'

def retrieve():
    urllib.urlretrieve(url, cachepath)

def extract(fp=cachepath):
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
    rows = rows[1:-1]
    # usually one last row with footnotes but some months stuff goes wrong and we
    # have extra rows and then something random e.g. april 2016 there is a
    # random number 20+ rows down
    rows = [ r for r in rows if r[0] != '' ]
    transposed = zip(*rows)
    # fix dates
    # delete "date fraction" column
    del transposed[5]
    transposed[0] = [ _fixdates(val) for val in transposed[0] ]
    for idx, row in enumerate(transposed[1:]):
        row = [ _fixup(val) for val in row ]
        transposed[idx+1] = row
    
    data = zip(*transposed)
    fout = open(out_filepath, 'w')
    writer = csv.writer(fout, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(data)

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

def process():
    retrieve()
    extract()

if __name__ == '__main__':
    # extract(cachepath)
    process()

