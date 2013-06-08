url = 'http://www.econ.yale.edu/~shiller/data/ie_data.xls'
cachepath = 'cache/shiller.xls'

import urllib
import datautil
import datautil.tabular
out_filepath = 'data/data.csv'

def execute():
    fp = retrieve()
    out = extract(fp)
    save(out, out_filepath)

def retrieve():
    urllib.urlretrieve(url, cachepath)
    return cachepath

def extract(fp):
    reader = datautil.tabular.XlsReader(fp)
    # print reader.info()
    tabdata = reader.read()
    out = datautil.tabular.TabularData()

    # headings spread across rows 2-8
    out.header = [
        'Date',
        'SP500',
        'Dividend',
        'Earnings',
        'Consumer Price Index',
        'Long Interest Rate',
        'Real Price',
        'Real Dividend',
        'Real Earnings',
        'P/E10'
        ]

    # first 8 rows are headers, last 2 rows are footnotes so trim them
    data = tabdata.data[8:-2]
    transposed = zip(*data)
    # fix dates
    # delete "date fraction" column
    del transposed[5]
    transposed[0] = [ _fixdates(val) for val in transposed[0] ]
    for idx, row in enumerate(transposed[1:]):
        row = [ _fixup(val) for val in row ]
        transposed[idx+1] = row
    
    out.data = zip(*transposed)
    return out

def save(tabdata, out_filepath):
    writer = datautil.tabular.CsvWriter()
    writer.write(tabdata, open(out_filepath, 'w'))

def _fixup(val):
    if val == 'NA':
        return ''
    elif val == '':
        return ''
    return round(val, 2)

def _fixdates(val):
    # 1879.03 = march, 1879.1 = october
    val = round(val,2)
    year = int(val)
    # add 0.0001 to ensure we don't have problems re rounding
    month = int(0.1 + (val - year) * 100)
    out = str(year) + '-' + str(month).zfill(2) + '-01'
    return out

if __name__ == '__main__':
    # out = extract(cachepath)
    # save(out, out_filepath)
    execute()

