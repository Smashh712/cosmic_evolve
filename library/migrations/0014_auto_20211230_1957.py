# Generated by Django 3.1.3 on 2021-12-30 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_auto_20211230_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book_info',
            name='description',
        ),
        migrations.RemoveField(
            model_name='book_info',
            name='image',
        ),
        migrations.RemoveField(
            model_name='book_info',
            name='isbn13',
        ),
        migrations.RemoveField(
            model_name='book_info',
            name='price',
        ),
        migrations.RemoveField(
            model_name='book_info',
            name='pubdate',
        ),
    ]
