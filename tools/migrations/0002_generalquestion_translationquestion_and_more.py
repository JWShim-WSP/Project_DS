# Generated by Django 4.2 on 2023-07-12 17:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(max_length=512)),
                ('ai_response', models.TextField(blank=True, max_length=1024, null=True)),
                ('created', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TranslationQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(max_length=512)),
                ('to_language', models.CharField(blank=True, choices=[('English', 'English'), ('Korean', 'Korean')], max_length=12, null=True)),
                ('to_other_language', models.CharField(blank=True, max_length=24, null=True)),
                ('ai_response', models.TextField(blank=True, max_length=1024, null=True)),
                ('created', models.DateField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='image',
            name='phrase',
        ),
        migrations.AddField(
            model_name='image',
            name='created',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='prompt',
            field=models.CharField(default=django.utils.timezone.now, max_length=1024),
            preserve_default=False,
        ),
    ]