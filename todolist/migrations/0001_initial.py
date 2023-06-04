# Generated by Django 4.2 on 2023-06-04 15:32

from django.db import migrations, models
import django.db.models.deletion
import todolist.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('priority', models.CharField(choices=[('1', 'High'), ('2', 'Middle'), ('3', 'Low')], default='High', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ToDoItemList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField(default=todolist.models.one_week_hence)),
                ('priority', models.CharField(choices=[('1', 'High'), ('2', 'Middle'), ('3', 'Low')], default='High', max_length=10)),
                ('item_completed', models.BooleanField(default=False)),
                ('todo_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.todolist')),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
    ]
