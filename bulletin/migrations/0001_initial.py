# Generated by Django 4.2 on 2023-06-04 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
                ('post_Date', models.DateField(auto_now_add=True)),
                ('update_Date', models.DateField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('content', models.TextField(max_length=4096)),
                ('likers', models.ManyToManyField(related_name='post_likers', to='profiles.profile')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('post_Date', models.DateTimeField(auto_now_add=True)),
                ('CommentPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulletin.bulletin')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='bulletin.comment')),
            ],
            options={
                'ordering': ['-post_Date'],
            },
        ),
    ]
