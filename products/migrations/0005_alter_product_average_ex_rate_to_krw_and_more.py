# Generated by Django 4.2 on 2023-07-03 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0004_alter_purchase_added_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='average_ex_rate_to_KRW',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='average_unit_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='average_unit_price_KRW',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('KRW', 'South Korean Won'), ('BTC', 'Bitcoin'), ('JPY', 'Japanese Yen'), ('CNY', 'Chinese Yuan'), ('GBP', 'British Pound Sterling')], max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='moq',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_supplier', to='customers.supplier'),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_added_price_KRW',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_net_price_KRW',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='added_price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='added_price_KRW',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='net_price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='net_price_KRW',
            field=models.FloatField(blank=True),
        ),
    ]
