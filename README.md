Desarrolado en python 3 en conjunto con el framewor django

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

#### Instalar sendmail
yum install sendmail -y

#### Instalar  Python 3.8
Guía: https://computingforgeeks.com/how-to-install-python-3-on-centos/

#### Instalar  Rabbitmql in Centos 8

Guía: https://www.rabbitmq.com/install-rpm.html

Comenzar servicio. Ejecutar.

 ```
/sbin/service rabbitmq-server start

/sbin/service rabbitmq-server status`
 ```

#### Instalar Posgresql

Guía: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-centos-8-es

Comenzar servicio. Ejecutar

`sudo systemctl start postgresql`

#### Instalar Pipenv

`python3 -m pip install pipenv`

#### Instalar Sendmail

`yum install sendmail -y`


## Instalación:

#### Clonar projecto

`git clone https://github.com/Joaquinecc/hips.git`

#### Instalar algunas dependencias
 ```
sudo yum groupinstall "Development Tools"

sudo yum install python3-devel

sudo yum install postgresql-libs

sudo yum install postgresql-devel
 ```
#### Archivo de Configuración (secrets.json)
 ```
{
    "allowed_hosts": ["localhost", "127.0.0.1","*"],
    "db_name": "db_name",
    "db_user": "db_user",
    "db_password": "db_password",
    "db_host": "localhost",
    "db_port": "db_port",
    "secret_key": "secret_key",
    "debug": true or false ,
    "ADMIN_EMAIL_ADDRESS":"example@email.com",
    "EMAIL_HOST_PASSWORD":"password123"
  }
 ```
#### Activar Entorno virtual.

`pipenv install`

#### Crear Tables

`python manage.py migrate`

#### Crear un usuario admin

`python manage.py createsuperuser`

#### Comenzar Servicios

Django.
`python manage.py runserver 0.0.0.0:80`

Celery worker
`celery -A hips worker -l INFO`

Calery beat
`celery -A hips beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`

#### Comenzar
Go to `http://localhost:8000/admin`to access the tool

