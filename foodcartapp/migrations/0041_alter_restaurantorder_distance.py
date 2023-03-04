# Generated by Django 4.1.6 on 2023-03-04 06:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_alter_order_status_alter_restaurantorder_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantorder',
            name='distance',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='расстояние'),
        ),
    ]