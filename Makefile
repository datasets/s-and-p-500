all: valid.txt

../archive:
	mkdir ../archive

../archive/shiller.xls: ../archive
	curl -o ../archive/shiller.xls "http://www.econ.yale.edu/~shiller/data/ie_data.xls"

../data:
	mkdir ../data    
    
../data/data.csv: ../data ../archive/shiller.xls process.py
	python process.py

valid.txt: ../data/data.csv ../datapackage.json test_data.py
	python test_data.py
	echo "Datapackage is valid" > valid.txt

.PHONY: all