# Generated by Django 3.1.3 on 2021-12-28 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_book_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_info',
            name='author',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='book_info',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='book_info',
            name='title',
            field=models.CharField(max_length=150),
        ),
    ]
