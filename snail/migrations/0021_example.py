# Generated by Django 4.1.7 on 2023-04-05 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snail', '0020_alter_payment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
    ]
