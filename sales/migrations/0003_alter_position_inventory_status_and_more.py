# Generated by Django 4.2 on 2023-06-25 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_position_inventory_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='inventory_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='position',
            name='position_sold',
            field=models.BooleanField(default=False),
        ),
    ]
