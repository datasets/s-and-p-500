url = 'http://www.econ.yale.edu/~shiller/data/ie_data.xls'
cache = 'cache'

import datautil
import datautil.tabular
cache = datautil.Cache(cache)
out_filepath = 'data/data.csv'

class Extractor(object):
    def execute(self):
        fp = cache.retrieve(url)
        reader = datautil.tabular.XlsReader(fp)
        # print reader.info()
        tabdata = reader.read()
        # clean up data
        data = tabdata.data
        # headings spread across rows 2-8
        headings = zip(*data[1:8])
        tabdata.header = [ ' '.join(cols).strip() for cols in headings ]
        data = tabdata.data[8:-1]
        transposed = zip(*data)
        # get rid of odd date e.g. 1871.01 and replace with date fraction
        fraction = transposed[5]
        del transposed[5]
        transposed[0] = fraction
        tabdata.data = zip(*transposed)
        del tabdata.header[5]
        del tabdata.header[0]
        tabdata.header.insert(0, 'Date')
        tabdata.header[1] = 'Price'
        tabdata.header[-1] = 'P/E10'
        writer = datautil.tabular.CsvWriter()
        writer.write(tabdata, open(out_filepath, 'w'))


if __name__ == '__main__':
    Extractor().execute()

