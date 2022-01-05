# Generated by Django 3.1.3 on 2022-01-05 12:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_auto_20220105_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfomation',
            name='startRent',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 1, 5, 12, 17, 57, 828042, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='createDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 1, 5, 12, 17, 57, 829044, tzinfo=utc)),
        ),
    ]