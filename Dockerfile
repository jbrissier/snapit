FROM ubuntu:18.04
MAINTAINER Jochen Brissier

RUN apt-get update
RUN apt-get install -y git python3-dev python3-git  python3-setuptools python3-pip libjpeg-dev zlib1g-dev libtiff-dev

RUN pip3 install gunicorn
RUN apt-get install -y supervisor


RUN apt-get -y install nginx


ADD supervisor.conf /opt/supervisor.conf

ADD requirements.txt /opt/requirements.txt
WORKDIR /opt/

RUN pip3 install -r requirements.txt

ADD . /opt/

RUN mkdir -p /opt/data/media

RUN python3 manage.py collectstatic --noinput --settings base.settings.prod

ADD nginx.conf /etc/nginx/nginx.conf
ADD nginx_default.conf /etc/nginx/sites-available/default
EXPOSE 80

#RUN sed -i 's/DEBUG = True/DEBUG = False/g' base/settings.py
# build database
RUN python3 manage.py migrate

CMD supervisord -c /opt/supervisor.conf -n
