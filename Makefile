
setup_project:
	sudo apt-get install python3.8 python3.8-venv
	python3.8 -m venv env3.8
	./env3.8/bin/python3.8 -m pip install --upgrade pip
	./env3.8/bin/python3.8 -m pip install -r requirements.txt

help:
	env3.8/bin/python3.8 mycommand.py -h

test:
	env3.8/bin/python3.8 mycommand.py "" --run-tests

run:
	env3.8/bin/python3.8 mycommand.py "https://drive.google.com/file/d/1y1MzCLpFioVAHnGNZDKG5L4O62PtCqZX/view?usp=sharing" --output-filename "output/line.jpg" --size "1400x1000" -gt "scatter"


freeze_requirements:
	./env3.8/bin/pip freeze > requirements.txt