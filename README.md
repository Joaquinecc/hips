# hips
So2 hips project class

Requiremente
Celery (https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html)
Rabbitmq
Posgresql
Djangop
python

celery -A hips worker -l INFO

 celery -A hips beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler