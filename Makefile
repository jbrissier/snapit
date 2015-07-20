project = base
app?=

ev = env
env= env/bin/activate

dumpdata:
	python2.7 ./manage.py dumpdata --indent 4 --natural auth --exclude auth.permission > $(project)/fixtures/bootstrap_auth.json
	python2.7 ./manage.py dumpdata --indent 4 --natural sites > $(project)/fixtures/bootstrap_sites.json


loaddata:
	python2.7 manage.py loaddata $(project)/fixtures/bootstrap_auth.json
	python2.7 manage.py loaddata $(project)/fixtures/bootstrap_sites.json

mm:
	. $(env); python2.7 manage.py makemigrations
	. $(env); python2.7 manage.py migrate

create-env:
	virtualenv env
	. $(env); pip install -r requirements.txt

first-build: create-env mm


flush:
	. $(env); python2.7 manage.py flush --noinput

rebuild: flush build

run:
	. $(env); python manage.py runserver

pip:
	. $(env); pip install -r requirements.txt

test:
	py.test $(app)
	#./manage.py test $(app) -v 2

shell:
	. $(env); python manage.py shell