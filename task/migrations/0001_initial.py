# Generated by Django 3.2.3 on 2021-05-26 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HashFil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=500)),
                ('path_file', models.CharField(max_length=500, unique=True)),
            ],
        ),
    ]
