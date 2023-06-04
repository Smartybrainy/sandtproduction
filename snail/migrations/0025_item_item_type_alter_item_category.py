# Generated by Django 4.1.7 on 2023-04-07 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snail', '0024_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.CharField(choices=[('SNAIL', 'Snail'), ('COSMETIC', 'Cosmetic')], default='SNAIL', max_length=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('GA', 'Giant African'), ('RO', 'Roman Snail'), ('MS', 'Mediterranean Snail'), ('BC', 'Body Cream'), ('BW', 'Body Wash'), ('BS', 'Black Soap'), ('LS', 'Liquid Soap'), ('FBL', 'Face & Body Lotion'), ('FBM', 'Face & Body Moisturiser')], max_length=3),
        ),
    ]