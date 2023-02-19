# Generated by Django 4.1.6 on 2023-02-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_order_called_order_completed'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='order',
            name='foodcartapp_phonenu_ea3b7f_idx',
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['phonenumber', 'firstname', 'lastname', 'address', 'status', 'called', 'completed'], name='foodcartapp_phonenu_ac1af6_idx'),
        ),
    ]
