from rest_framework import serializers

from .models import Order, ProductOrder


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'products',
            'firstname',
            'lastname',
            'phonenumber',
            'address'
            ]
