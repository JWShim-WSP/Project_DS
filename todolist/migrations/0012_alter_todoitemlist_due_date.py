# Generated by Django 4.2 on 2023-05-27 07:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0011_alter_todoitemlist_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitemlist',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 3, 7, 56, 29, 483104, tzinfo=datetime.timezone.utc)),
        ),
    ]
