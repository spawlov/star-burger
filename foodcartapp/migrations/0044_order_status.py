# Generated by Django 4.1.6 on 2023-02-19 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_auto_20230219_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PRC', 'Необработан'), ('PRC', 'Завершен')], default='PRC', max_length=3, verbose_name='статус заказа'),
        ),
    ]