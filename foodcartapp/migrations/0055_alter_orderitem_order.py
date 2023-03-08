# Generated by Django 4.1.6 on 2023-03-08 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0054_alter_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_no', to='foodcartapp.order', verbose_name='заказ'),
        ),
    ]