# Generated by Django 3.0.4 on 2020-08-24 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20200824_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproducts',
            name='slug',
        ),
    ]
