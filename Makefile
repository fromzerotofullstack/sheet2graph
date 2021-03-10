
setup_project:
	sudo apt-get install python3.8 python3.8-venv
	python3.8 -m venv env3.8
	./env3.8/bin/python3.8 -m pip install --upgrade pip
	./env3.8/bin/python3.8 -m pip install -r requirements.txt

help:
	env3.8/bin/python3.8 mycommand.py -h

run:
	#env3.8/bin/python3.8 mycommand.py sales_data.csv
	#env3.8/bin/python3.8 mycommand.py sales_data.csv --graph-type "line"
	#env3.8/bin/python3.8 mycommand.py sales_data.csv --graph-type "line" --output-folder "sales/graphs"
	#env3.8/bin/python3.8 mycommand.py sales_data.csv --graph-type "line" --output-filename "output2/line.png"
	#env3.8/bin/python3.8 mycommand.py sales_data.csv -gt "bar" -ofi "output2/bar2.png"
	#env3.8/bin/python3.8 mycommand.py sales_data.csv --output-format "svg"
	env3.8/bin/python3.8 mycommand.py sales_data.csv --output-format "jpg"
	#env3.8/bin/python3.8 mycommand.py sales_data.csv --output-format "svg" --output-filename "output2/line.jpg"


freeze_requirements:
	./env3.8/bin/pip freeze > requirements.txt