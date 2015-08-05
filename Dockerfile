FROM ubuntu:14.04
MAINTAINER jochen brissier

RUN echo "1" > /tmp/1.txt

RUN apt-get update
RUN apt-get install -y git python-dev python-git  python-setuptools libjpeg
RUN easy_install pip

#RUN pip install pyodbc==3.0.6 --allow-unverified pyodbc --allow-all-external



#ADD .odbc.ini /etc/odbc.ini
#ADD .odbcinst.ini /etc/odbcinst.ini
#ADD .freetds.conf /etc/freetds/freetds.conf





RUN apt-get install -y gunicorn
RUN apt-get install -y supervisor


RUN apt-get -y install nginx


ADD supervisor.conf /opt/supervisor.conf

ADD requirements.txt /opt/requirements.txt
WORKDIR /opt/

RUN pip install -r requirements.txt

ADD . /opt/

RUN python manage.py collectstatic --noinput

ADD nginx.conf /etc/nginx/nginx.conf
ADD nginx_default.conf /etc/nginx/sites-available/default
EXPOSE 80

RUN sed -i 's/DEBUG = True/DEBUG = False/g' base/settings.py

CMD supervisord -c /opt/supervisor.conf -n
