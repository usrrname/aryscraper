PYTHON = python3
PIP = pip3
init:
	${PIP} install -r requirements.txt
run:
	${PYTHON} main.py
venv: # setup a virtual environment
	${PYTHON} -m venv venv
clean:
	rm -rf __pycache__
	 rm -rf venv
# This function uses pytest to test our source files
test:
	${PYTHON} -m pytest