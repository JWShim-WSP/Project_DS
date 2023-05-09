# Generated by Django 4.2 on 2023-05-09 01:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarwithevent', '0004_alter_event_end_time_alter_event_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]