FROM python:3.9.19-bullseye

RUN pip3 install --upgrade pip 
#python

RUN pip install flask flask-mysqldb mysql-connector-python
#translation flask-sql

RUN mkdir -p /srv/templates

COPY index.html /srv/templates
COPY inscription.html /srv/templates
COPY connexion.html /srv/templates

COPY app.py /srv
CMD ["flask","--app","/srv/app","run","--host=0.0.0.0"]
