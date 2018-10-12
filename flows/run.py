from dataflows import Flow, PackageWrapper, ResourceWrapper, validate
from dataflows import add_metadata, dump_to_path, load, set_type, find_replace, printer


def rename(package: PackageWrapper):
    package.pkg.descriptor['resources'][0]['name'] = 's-and-p'
    package.pkg.descriptor['resources'][0]['path'] = 'data/s-and-p.csv'
    package.pkg.descriptor['resources'][0]['title'] = 'S&P 500'
    yield package.pkg
    res_iter = iter(package)
    first: ResourceWrapper = next(res_iter)
    yield first.it
    yield from package


finance_vix = Flow(
    add_metadata(
        name="s-and-p-500",
        title= "Standard and Poor's (S&P) 500 Index Data including Dividend, Earnings and P/E Ratio",
        sources=[
            {
                "name": "Robert Shiller",
                "web": "http://www.econ.yale.edu/~shiller/data.htm",
                "title": "Robert Shiller"
            }
        ],
        licenses=[
            {
                "id": "odc-pddl",
                "name": "public_domain_dedication_and_license",
                "version": "1.0",
                "url": "http://opendatacommons.org/licenses/pddl/1.0/"
            }
        ],
        maintainers=[{"name": "Rufus Pollock","email": "rufus.pollock@okfn.org"}],
        keywords=["Indicator","Economics","Prices","Stocks","Stock Market","US"],
        version="0.2.0",
        related=[
            {
              "title": "S&P 500 Companies",
              "path": "/core/s-and-p-500-companies",
              "publisher": "core",
              "formats": ["CSV", "JSON"]
            },
            {
              "title": "S&P 500 Companies with Financial Information",
              "path": "/core/s-and-p-500-companies-financials",
              "publisher": "core",
              "formats": ["CSV", "JSON"]
            },
            {
              "title": "VIX - CBOE Volatility Index",
              "path": "/core/finance-vix",
              "publisher": "core",
              "formats": ["CSV", "JSON"]
            },
            {
              "title": "NYSE and Other Listings",
              "path": "/core/nyse-other-listings",
              "publisher": "core",
              "formats": ["CSV", "JSON"]
            }
        ],
        views=[
            {
                "name": "graph",
                "title": "Level ('price') of the S&P 500 index",
                "specType": "simple",
                "spec": {"type": "line","group": "Date","series": ["SP500"]}
            }
        ]
    ),
    load(
        load_source='http://www.econ.yale.edu/~shiller/data/ie_data.xls',
        format='xls',
        sheet='Data',
        skip_rows=[-1,2,3,4,5,6,7,8],
        headers=[
            "Date",
            "SP500",
            "Dividend",
            "Earnings",
            "Consumer",
            "Price Index",
            "Long Interest Rate",
            "Real Price",
            "Real Dividend",
            "Real Earnings",
            "PE10"
        ]
    ),
    find_replace(fields=[
            {'name': 'CAPE', 'patterns': [{'find': 'NA', 'replace': ''}]},
        ],
    ),
    set_type('PE10', type='number'),
    rename,
    validate(),
    printer(),
    dump_to_path(),
)


if __name__ == '__main__':
    finance_vix.process()
