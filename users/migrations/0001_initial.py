# Generated by Django 3.2.9 on 2021-12-14 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nickname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=300, unique=True)),
                ('profile_image_url', models.CharField(max_length=2000)),
                ('host', models.BooleanField(default=False)),
                ('host_description', models.CharField(max_length=300, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('context', models.CharField(max_length=300)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.program')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.user')),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.program')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'likes',
            },
        ),
    ]
