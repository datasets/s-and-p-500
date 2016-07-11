all: pushed.txt

../archive:
	mkdir ../archive

../archive/shiller.xls: ../archive
	curl -o ../archive/shiller.xls "http://www.econ.yale.edu/~shiller/data/ie_data.xls"

../data:
	mkdir ../data    
    
../data/data.csv: ../data ../archive/shiller.xls extract.py
	python extract.py

valid.txt: ../data/data.csv ../datapackage.json test_data.py
	python test_data.py
	echo "Datapackage is valid" > valid.txt

pushed.txt: valid.txt ../archive/shiller.xls
	git add ../data/data.csv
	git commit -m "[data][skip ci] automatic update" || exit 0
	git push publish
	echo "Update has been pushed if there was a change" > pushed.txt

.PHONY: all