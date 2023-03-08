# Generated by Django 4.1.6 on 2023-03-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_rename_productorder_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('WAITING', 'Необработан'), ('PROCESS', 'Готовится'), ('COMPLETED', 'Завершен')], db_index=True, default='WAITING', max_length=10, verbose_name='статус заказа'),
        ),
    ]
