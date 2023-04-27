# Generated by Django 3.0.7 on 2020-06-19 08:36

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foodcartapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'город', 'verbose_name_plural': 'города'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'клиент', 'verbose_name_plural': 'клиенты'},
        ),
        migrations.AlterModelOptions(
            name='hotel',
            options={'verbose_name': '???', 'verbose_name_plural': '???'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': '???', 'verbose_name_plural': '???'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'заказ', 'verbose_name_plural': 'заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderdetails',
            options={'verbose_name': 'позиция заказа', 'verbose_name_plural': 'позиции заказов'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.RemoveField(
            model_name='city',
            name='state',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='gst',
        ),
        migrations.RemoveField(
            model_name='location',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='product',
            name='half_price',
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=50, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(max_length=256, verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=10, verbose_name='телефон'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user',
            field=models.OneToOneField(blank=True, help_text='если зарегистрирован на сайте',
                                       null=True, on_delete=django.db.models.deletion.SET_NULL,
                                       related_name='customer', to=settings.AUTH_USER_MODEL,
                                       verbose_name='учётка'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='hoteladmin',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='administrated_hotels',
                                    to='foodcartapp.CustomUser', verbose_name='администратор'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='hotels', to='foodcartapp.Location'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=models.CharField(max_length=50, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='cities', to='foodcartapp.City',
                                    verbose_name='город'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=50, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='стоимость'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='orders', to='foodcartapp.CustomUser',
                                    verbose_name='заказчик'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.DateTimeField(blank=True, db_index=True, null=True,
                                       verbose_name='доставлено'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now,
                                       verbose_name='заказано'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.SmallIntegerField(db_index=True, default=1, verbose_name='тип заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(db_index=True, default=1, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='positions', to='foodcartapp.Order',
                                    verbose_name='заказ'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='order_positions', to='foodcartapp.Product',
                                    verbose_name='товар'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='product',
            name='availabilty',
            field=models.BooleanField(db_index=True, default=True, verbose_name='в продаже'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=50, verbose_name='категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='full_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='products', to='foodcartapp.Hotel'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='картинка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='special_status',
            field=models.BooleanField(db_index=True, default=False,
                                      verbose_name='спец.предложение'),
        ),
    ]
