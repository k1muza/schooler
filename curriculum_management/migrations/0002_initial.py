# Generated by Django 4.2.4 on 2024-04-28 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school_management', '0001_initial'),
        ('curriculum_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='syllabus',
            name='levels',
            field=models.ManyToManyField(to='school_management.level'),
        ),
        migrations.AddField(
            model_name='syllabus',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum_management.subject'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='klass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_management.class'),
        ),
    ]
