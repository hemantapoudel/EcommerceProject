# Generated by Django 3.0.4 on 2020-08-24 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_remove_orderproducts_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]
