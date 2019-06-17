test:
	coverage run --source sports setup.py test
	coverage report -m
	rm -fr sports.py.egg-info .coverage
checkstyle:
	flake8 --ignore==E501, E401, E403
publish:
	pip install --upgrade twine setuptools wheel
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build sit .egg sports.py.egg-info
