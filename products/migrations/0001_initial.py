# Generated by Django 4.2 on 2023-06-05 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('image', models.ImageField(default='no_picture.png', upload_to='products')),
                ('price', models.FloatField(help_text='in US dollars $')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('remark', models.TextField(blank=True, max_length=1024)),
                ('product_type', models.CharField(choices=[('Sensor', 'Sensor'), ('Plasma Torch', 'Plasma Torch'), ('Pump', 'Pump'), ('Pressure', 'Pressure'), ('Etc', 'Etc')], max_length=50)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
