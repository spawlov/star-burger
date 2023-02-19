# Generated by Django 4.1.6 on 2023-02-19 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='called',
            field=models.DateTimeField(blank=True, null=True, verbose_name='звонок клиенту'),
        ),
        migrations.AddField(
            model_name='order',
            name='completed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='доставлен'),
        ),
    ]