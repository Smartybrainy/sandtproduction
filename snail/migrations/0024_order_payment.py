# Generated by Django 4.1.7 on 2023-04-05 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snail', '0023_payments_remove_payment_user_remove_order_payment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='snail.payments'),
        ),
    ]
