# Generated by Django 3.1.3 on 2022-01-06 14:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_auto_20220105_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfomation',
            name='startRent',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 1, 6, 14, 29, 5, 795820, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='createDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 1, 6, 14, 29, 5, 796820, tzinfo=utc)),
        ),
    ]
