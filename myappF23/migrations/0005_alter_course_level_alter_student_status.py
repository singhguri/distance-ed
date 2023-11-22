# Generated by Django 4.2.6 on 2023-10-04 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myappF23', '0004_remove_instructor_course_course_instructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('BE', 'Beginner'), ('IN', 'Intermediate'), ('AD', 'Advanced')], default='BE', max_length=10),
        ),
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(choices=[('ER', 'Enrolled'), ('SP', 'Suspended'), ('GD', 'Graduated')], default='ER', max_length=10),
        ),
    ]