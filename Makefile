
setup_project:
	sudo apt-get install python3.8 python3.8-venv
	python3.8 -m venv env3.8
	./env3.8/bin/python3.8 -m pip install --upgrade pip
	./env3.8/bin/python3.8 -m pip install -r requirements.txt

help:
	env3.8/bin/python3.8 mycommand.py -h

run:
	#env3.8/bin/python3.8 mycommand.py sales_data.csv
	env3.8/bin/python3.8 mycommand.py sales_data.csv --graph-type "line"


freeze_requirements:
	./env3.8/bin/pip freeze > requirements.txt