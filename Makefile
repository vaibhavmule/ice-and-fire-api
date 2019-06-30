init:
	pip install -r requirements.txt
test:
	./manage.py test books
coverage:
	coverage run --source='./books' manage.py test books
	coverage report
