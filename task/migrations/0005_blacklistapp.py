# Generated by Django 3.2.3 on 2021-05-30 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_whitelistuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=500, unique=True)),
            ],
        ),
    ]
