# Generated by Django 4.1.6 on 2023-02-19 06:12

from django.db import migrations, transaction


def set_default_price(apps, schema_editor):
    Product = apps.get_model('foodcartapp', 'Product')
    ProductOrder = apps.get_model('foodcartapp', 'ProductOrder')
    with transaction.atomic():
        for product in ProductOrder.objects.all():
            if not product.price:
                default_price = Product.objects.get(
                    pk=product.product_id
                ).price
                product.price = default_price
                product.save()


class Migration(migrations.Migration):
    dependencies = [
        ('foodcartapp', '0041_alter_restaurantorder_distance'),
    ]

    operations = [
        migrations.RunPython(set_default_price)
    ]
