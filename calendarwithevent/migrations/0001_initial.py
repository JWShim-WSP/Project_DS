# Generated by Django 4.2 on 2023-06-29 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('event_completed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
    ]
