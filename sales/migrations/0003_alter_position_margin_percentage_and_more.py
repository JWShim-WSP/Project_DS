# Generated by Django 4.2 on 2023-07-03 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_sale_delivery_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='margin_percentage',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='net_price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='net_profit',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='delivery_cost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='extra_cost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='final_profit',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_net_price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_net_profit',
            field=models.FloatField(blank=True),
        ),
    ]
