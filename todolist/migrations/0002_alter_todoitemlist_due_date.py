# Generated by Django 4.2 on 2023-05-27 06:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitemlist',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 3, 6, 30, 4, 489929, tzinfo=datetime.timezone.utc)),
        ),
    ]
