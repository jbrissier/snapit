project = base
app?=

ev = env
env= env/bin/activate



name = snapit
version = 0.0.1

maintainer = jbrissier
tag = $(maintainer)/$(name):$(version)


dumpdata:
	python ./manage.py dumpdata --indent 4 --natural auth --exclude auth.permission > $(project)/fixtures/bootstrap_auth.json
	python ./manage.py dumpdata --indent 4 --natural sites > $(project)/fixtures/bootstrap_sites.json


loaddata:
	python manage.py loaddata $(project)/fixtures/bootstrap_auth.json
	python manage.py loaddata $(project)/fixtures/bootstrap_sites.json

mm:
	pipenv run python manage.py makemigrations
	pipenv run python manage.py migrate

create-env:
	virtualenv env
	pipenv run pip install -r requirements.txt

first-build: create-env mm


flush:
	pipenv run python manage.py flush --noinput

rebuild: flush build

run:
	pipenv run python manage.py runserver

pip:
	pipenv run pip install -r requirements.txt

test:
	py.test $(app)
	#./manage.py test $(app) -v 2

shell:
	pipenv run python manage.py shell

docker-build: *
	docker build -t $(tag) .

docker-run: docker-build
	docker run -d --name $(name) -p 80:80 $(tag)

docker-rm:
	docker rm -f $(name)
