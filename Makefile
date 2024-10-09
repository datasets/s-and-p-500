all: valid.txt

../archive:
	mkdir ../archive

../archive/shiller.xls: ../archive
	curl -o ../archive/shiller.xls "http://www.econ.yale.edu/~shiller/data/ie_data.xls"

../data:
	mkdir ../data    
    
../data/data.csv: ../data ../archive/shiller.xls scripts/process.py
	python scripts/process.py

valid.txt: ../data/data.csv datapackage.json scripts/test_data.py
	python scripts/test_data.py
	echo "Datapackage is valid" > valid.txt

.PHONY: all