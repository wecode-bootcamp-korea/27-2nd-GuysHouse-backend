# Generated by Django 3.1.2 on 2021-12-17 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='DetailImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=2000)),
            ],
            options={
                'db_table': 'detail_images',
            },
        ),
        migrations.CreateModel(
            name='Logging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('previous_url', models.CharField(max_length=2000)),
            ],
            options={
                'db_table': 'loggings',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=300)),
                ('supply', models.CharField(max_length=300)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('limit', models.PositiveSmallIntegerField(default=1)),
                ('count', models.SmallIntegerField(default=0)),
                ('thumbnail_image_url', models.CharField(max_length=2000)),
                ('start_date', models.DateTimeField()),
                ('running_time', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'programs',
            },
        ),
        migrations.CreateModel(
            name='ProgramCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'program_categories',
            },
        ),
        migrations.CreateModel(
            name='ProgramQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'program_questions',
            },
        ),
        migrations.CreateModel(
            name='ScreeningQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
                ('program', models.ManyToManyField(through='programs.ProgramQuestion', to='programs.Program')),
            ],
            options={
                'db_table': 'screening_questions',
            },
        ),
        migrations.CreateModel(
            name='ScreeningAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=300)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='programs.screeningquestion')),
            ],
            options={
                'db_table': 'screening_answers',
            },
        ),
    ]
