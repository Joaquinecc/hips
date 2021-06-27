# HIPS SO 2 PROJECT
Trabajo Practico de la clase SO2. Diseño de un sistema hips.
Funciones:
1. Verificar si hubo modificaciones en archivos seleccionados.
2. Verificar los usuarios que están conectados. Y desde que origen.
3. Verifica si hay sniffers o si el equipo ha entrado en modo promiscuo.
4. Busca patrones de intrusion en los siguiente los: /var/log/secure,maillog,message . Servicio = smpt.
5. Identifica patrones de multiples acceso a paginas desconocidas
6. Verifica la cola mail
7. Prevenciónt de procesos sospechoso por el patron de consumo de memoria ram y cpu
8. Prevención de archivos script en el directorio /tmp
9. Prevención de ataque DDos dns.
10. Prevención de scripts ejecutandos como cron.
11. Prevención de multiples acceso fallido.Servicio = sshd

## Dependecias:

1. Rabbitmq (as broker)
2. Posgresql
3. Django
4. Python 3.8
5. Pipenv
6. Sendmail(Cola de mail )
7. iptable (Bloqueo de Ip)

## Guia de instalación diseñado para SO centos 8

#### Instalar iptable. 
Guía: https://linuxize.com/post/how-to-install-iptables-on-centos-7/

#### Instalarsendmail
yum install sendmail -y

#### Instalar  Python 3.8
Guía: https://computingforgeeks.com/how-to-install-python-3-on-centos/

#### Instalar  Rabbitmql in Centos 8

Guía:https://www.rabbitmq.com/install-rpm.html

Comenzar servicio. Ejecutar.

`/sbin/service rabbitmq-server start`

`/sbin/service rabbitmq-server status`

#### Instalar Posgresql

Guía: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-centos-8-es

Comenzar servicio. Ejecutar

`sudo systemctl start postgresql`

#### Instalar Pipenv

`python3 -m pip install pipenv`

#### Instalar Sendmail

`yum install sendmail -y`


## Intalación:

#### Clonar projecto

`git clone https://github.com/Joaquinecc/hips.git`

Install some dependecies 

sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
sudo yum install postgresql-libs
sudo yum install postgresql-devel

Then run
pipenv install

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver 0.0.0.0:80

celery -A hips worker -l INFO

celery -A hips beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler


if choose to use postrgres user

change to md5
/var/lib/pgsql/9.3/data/pg_hba.conf

https://stackoverflow.com/questions/11339917/django-operationalerror-fatal-ident-authentication-failed-for-user-usernam
yum install sendmail -y
