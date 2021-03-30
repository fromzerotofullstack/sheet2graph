
setup_project:
	sudo apt-get install python3.8 python3.8-venv
	python3.8 -m venv env3.8
	./env3.8/bin/python3.8 -m pip install --upgrade pip
	./env3.8/bin/python3.8 -m pip install -r requirements.txt

help:
	env3.8/bin/python3.8 ./src/sheet2graph/sheet2graph.py -h

test:
	env3.8/bin/python3.8 ./src/sheet2graph/sheet2graph.py --run-tests

run:
	env3.8/bin/python3.8 ./src/sheet2graph/sheet2graph.py ./test_data/sales_data.xlsx -x "a3:a6" -y "b3:b6" --output-filename output/tests/out.png -xlabel "Salesmen" -ylabel "Sales Week 1" --print-only
	#env3.8/bin/python3.8 ./src/sheet2graph/sheet2graph.py ./test_data/sales_data.xlsx -x "a3:a6" -y "b3:b6" --output-filename output/tests/out.png -xlabel "Salesmen" -ylabel "Sales Week 1"


package:
	rm -rf ./dist
	rm -rf ./build
	env3.8/bin/python3.8 -m pip install --upgrade build
	env3.8/bin/python3.8 -m build

package_upload:
	env3.8/bin/python3.8 -m pip install --upgrade twine
	#env3.8/bin/python3.8 -m twine upload --repository testpypi dist/*
	env3.8/bin/python3.8 -m twine upload dist/*


package_install:
	rm -rf ./test_env3
	python3.8 -m venv test_env3.8
	./test_env3.8/bin/python3.8 -m pip install --upgrade pip
	#./test_env3.8/bin/python3.8 -m pip install --no-deps -i https://test.pypi.org/simple/ sheet2graph==0.1.59
	./test_env3.8/bin/python3.8 -m pip install sheet2graph

package_uninstall:
	./test_env3.8/bin/python3.8 -m pip uninstall sheet2graph


freeze_requirements:
	./env3.8/bin/pip freeze > requirements.txt