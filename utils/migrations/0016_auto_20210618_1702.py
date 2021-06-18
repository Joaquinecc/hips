# Generated by Django 3.2.4 on 2021-06-18 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0015_rename_procesconsumelimit_processconsumelimit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processconsumelimit',
            old_name='qty',
            new_name='max_cpu',
        ),
        migrations.AddField(
            model_name='processconsumelimit',
            name='max_ram',
            field=models.PositiveBigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
