# Generated by Django 3.2.9 on 2021-12-22 20:42

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
                ('kakao_id', models.CharField(max_length=100, unique=True)),
                ('nickname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=300, null=True)),
                ('profile_image_url', models.CharField(max_length=2000)),
                ('is_host', models.BooleanField(default=False)),
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
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
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
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('user_id', 'program_id'), name='unique reviews'),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('user_id', 'program_id'), name='unique likes'),
        ),
    ]
