# Generated by Django 4.2.6 on 2023-11-24 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myappF23', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='date_of_birth',
        ),
    ]