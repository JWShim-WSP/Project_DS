# Generated by Django 4.2 on 2023-05-16 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('Sensor', 'Sensor'), ('Plasma Torch', 'Plasma Torch'), ('Pump', 'Pump'), ('Etc', 'Etc')], max_length=50),
        ),
    ]
