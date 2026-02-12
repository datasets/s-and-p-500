all: valid.txt

FRED_SP500_URL = https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500

archive:
	mkdir -p archive

archive/fred_sp500.csv: archive
	curl -L "$(FRED_SP500_URL)" -o archive/fred_sp500.csv

data:
	mkdir -p data

data/data.csv: data archive/fred_sp500.csv scripts/update_from_fred.py
	python scripts/update_from_fred.py

valid.txt: data/data.csv datapackage.json scripts/test_data.py
	python scripts/test_data.py
	echo "Datapackage is valid" > valid.txt

.PHONY: all
