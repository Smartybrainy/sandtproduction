# Generated by Django 4.1.7 on 2023-04-03 04:04

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('snail', '0009_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='shipping_country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
