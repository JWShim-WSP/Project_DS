# Generated by Django 4.2 on 2023-06-06 20:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sale',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
