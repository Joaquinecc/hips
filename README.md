# hips
So2 hips project class

Dependecies:
Celery (https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html)
Rabbitmq
Posgresql
Djangop
python 3.8
Git
Pipenv


Install python python 3.8
Follow guide 
https://computingforgeeks.com/how-to-install-python-3-on-centos/

Installing Rabbitmql in Centos 8

Follow guide on 

https://www.rabbitmq.com/install-rpm.html
To start service 
/sbin/service rabbitmq-server start

/sbin/service rabbitmq-server status



Posgresql

Follow Guide to install
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-centos-8-es

Start service

sudo systemctl start postgresql





intal Git

sudo dnf install git-all



Install Pipenv
python3 -m pip install pipenv




 https://www.techbrown.com/bash-script-install-qmail-server-centos-rhel/



 After installing all dependecies of the project

Create Database

sudo -i -u postgres

First Create a databse and edi teh secret.json



 Clone de project

git <link>

Install some dependecies 

sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
sudo yum install postgresql-libs
sudo yum install postgresql-devel

Then run
pipenv install

python manage.py migrate

python manage.py createsuper user

python manage.py runserver

celery -A hips worker -l INFO

celery -A hips beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler


if choose to use postrgres user

change to md5
/var/lib/pgsql/9.3/data/pg_hba.conf

https://stackoverflow.com/questions/11339917/django-operationalerror-fatal-ident-authentication-failed-for-user-usernam
