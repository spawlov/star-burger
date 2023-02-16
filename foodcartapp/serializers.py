from rest_framework import serializers

from .models import Order, ProductOrder


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.ListField(
        child=ProductOrderSerializer(),
        allow_empty=False,
    )

    class Meta:
        model = Order
        fields = [
            'products',
            'firstname',
            'lastname',
            'phonenumber',
            'address'
        ]
