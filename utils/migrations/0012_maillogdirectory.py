# Generated by Django 3.2.3 on 2021-06-09 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0011_httpacceslogdirectory'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailLogDirectory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=500)),
            ],
        ),
    ]