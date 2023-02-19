from rest_framework import serializers

from .models import Order, ProductOrder, Product


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ['product', 'quantity']

    def to_representation(self, products):
        return {'product': products.product.id, 'quantity': products.quantity}


class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'products',
            'firstname',
            'lastname',
            'phonenumber',
            'address'
        ]


class OrderSerializerResponse(serializers.ModelSerializer):
    products = ProductOrderSerializer(source='order', many=True)

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
