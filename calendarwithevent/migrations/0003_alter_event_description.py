# Generated by Django 4.2 on 2023-07-04 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarwithevent', '0002_alter_event_description_alter_event_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
