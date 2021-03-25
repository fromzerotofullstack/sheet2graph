
setup_project:
	sudo apt-get install python3.8 python3.8-venv
	python3.8 -m venv env3.8
	./env3.8/bin/python3.8 -m pip install --upgrade pip
	./env3.8/bin/python3.8 -m pip install -r requirements.txt

help:
	env3.8/bin/python3.8 mycommand.py -h

test:
	env3.8/bin/python3.8 mycommand.py --run-tests

run:
	#env3.8/bin/python3.8 mycommand.py --version
	#env3.8/bin/python3.8 mycommand.py
	#env3.8/bin/python3.8 mycommand.py sales_data.csv --print-only
	#env3.8/bin/python3.8 mycommand.py sales_data.csv
	#env3.8/bin/python3.8 mycommand.py sales_data.csv -x "a2:a6" -y "b2:b6"
	#env3.8/bin/python3.8 mycommand.py sales_data.csv -x "a3,a4,a5" -y "b3,b4,b5" --print-only
	#env3.8/bin/python3.8 mycommand.py sales_data.csv -x "a3,a4,a5" -y "b3,b4,b5"
	#env3.8/bin/python3.8 mycommand.py sales_data.csv -x "a3:a6" -y "b3:b6"
	env3.8/bin/python3.8 mycommand.py sales_data.xlsx -x "a3:a6" -y "b3:b6" --output-filename output/tests/out.png


freeze_requirements:
	./env3.8/bin/pip freeze > requirements.txt