# Generated by Django 4.1.7 on 2023-04-07 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snail', '0025_item_item_type_alter_item_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cosmetic',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Cosmetic Item List',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('snail.item',),
        ),
    ]