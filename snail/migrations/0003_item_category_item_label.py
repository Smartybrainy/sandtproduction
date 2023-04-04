# Generated by Django 4.1.7 on 2023-03-30 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snail', '0002_alter_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('GA', 'Giant African'), ('RO', 'Roman Snail'), ('MS', 'Mediterranean Snail')], default='GA', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], default='P', max_length=1),
            preserve_default=False,
        ),
    ]
