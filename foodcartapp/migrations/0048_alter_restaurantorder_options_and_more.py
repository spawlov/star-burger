# Generated by Django 4.1.6 on 2023-03-06 19:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_remove_order_foodcartapp_phonenu_6b5d7a_idx_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restaurantorder',
            options={'ordering': ['distance'], 'verbose_name': 'ресторан готовящий заказ', 'verbose_name_plural': 'рестораны готовящие заказ'},
        ),
        migrations.AlterField(
            model_name='restaurantorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_num', to='foodcartapp.order', verbose_name='заказ'),
        ),
    ]
