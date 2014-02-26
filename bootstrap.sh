#!/usr/bin/env bash

apt-get update
apt-get upgrade -y
apt-get install -y apache2 postgresql postgresql-contrib python-django python-numpy python-psycopg2
sudo su - postgres
createdb webgui
createuser webgui -P
echo 'SurveyPlot12'
echo 'SurveyPlot12'
#echo 'n'
#echo 'n'
#echo 'n'
#psql
#GRANT ALL PRIVILEGES ON DATABASE webgui TO webgui;
#\q
#cd /vagrant
#python manage.py syncdb

exit
