# Generated by Django 4.2 on 2023-06-02 14:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0005_alter_todoitemlist_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitemlist',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 9, 14, 15, 14, 262520, tzinfo=datetime.timezone.utc)),
        ),
    ]