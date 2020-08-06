manual:
	(cd docs; python3 site.py)
	cp docs/*.svg docs/output/
	cp docs/*.png docs/output/
deps:
	pip3 install -r requirements.txt
pyflakes:
	pyflakes
test:
	PYTHONPATH=. python3 tests/assembly.py
pytest:
	PYTHONPATH=. python3 tests/*.py
pep8:
	pep8 -r --ignore=E202,E501,E221,W291,W391,E302,E251,E203,W293,E231,E303,E201,E225,E261,E241 warpseq/ 
