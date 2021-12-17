# Generated by Django 3.1.2 on 2021-12-17 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='screeninganswer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user'),
        ),
        migrations.AddField(
            model_name='programquestion',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.program'),
        ),
        migrations.AddField(
            model_name='programquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.screeningquestion'),
        ),
        migrations.AddField(
            model_name='programcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.category'),
        ),
        migrations.AddField(
            model_name='programcategory',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.program'),
        ),
        migrations.AddField(
            model_name='program',
            name='categories',
            field=models.ManyToManyField(through='programs.ProgramCategory', to='programs.Category'),
        ),
        migrations.AddField(
            model_name='program',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
        migrations.AddField(
            model_name='logging',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.program'),
        ),
        migrations.AddField(
            model_name='detailimage',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.program'),
        ),
    ]