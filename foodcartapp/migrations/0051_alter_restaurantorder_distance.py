# Generated by Django 4.1.6 on 2023-03-07 03:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_alter_productorder_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantorder',
            name='distance',
            field=models.FloatField(default=100, validators=[django.core.validators.MinValueValidator(0)], verbose_name='расстояние'),
        ),
    ]
