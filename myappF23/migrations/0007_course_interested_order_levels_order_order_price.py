# Generated by Django 4.2.6 on 2023-11-08 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myappF23', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='levels',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='order_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
    ]
