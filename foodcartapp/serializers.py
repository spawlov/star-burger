from rest_framework import serializers

from .geocoder import calculate_distance
from .models import (
    Order,
    OrderItem,
    Restaurant,
    RestaurantMenuItem,
    RestaurantOrder,
)


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity',
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'address',
            'products'
        ]

    def validate_products(self, products):
        if len(products) < 1:
            raise serializers.ValidationError(
                {'error': 'Список продуктов не может быть пустым'}
            )
        return products

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        order_products = [OrderItem(
            order=order,
            price=product_data['product'].price,
            **product_data
        ) for product_data in products_data]
        OrderItem.objects.bulk_create(order_products)

        result_restaurants = None
        for product in OrderItem.objects.filter(order=order):
            restaurants = list(RestaurantMenuItem.objects.filter(
                product_id=product.product_id,
                availability=True
            ).values_list('restaurant', flat=True))
            if not result_restaurants:
                result_restaurants = restaurants
            set_restaurants = set(result_restaurants).intersection(set(restaurants))
            result_restaurants = list(set_restaurants)
            if not set_restaurants:
                break

        restaurants_list = Restaurant.objects.filter(pk__in=result_restaurants)
        for restaurant in restaurants_list:
            distance = calculate_distance(
                restaurant.address,
                order.address
            )
            RestaurantOrder.objects.create(
                order=order,
                restaurant=restaurant,
                distance=distance
            )
        return order


class OrderSerializerResponse(serializers.ModelSerializer):
    """The serializer is NOT used to create an object, only to output data"""
    products = ProductOrderSerializer(
        source='order_no', many=True, required=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'firstname',
            'lastname',
            'phonenumber',
            'address',
            'products'
        ]


class RestaurantListSerializer(serializers.ModelSerializer):
    restaurant = serializers.CharField(source='restaurant.name', required=True)

    class Meta:
        model = RestaurantOrder
        fields = ['restaurant', 'distance']


class OrderListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    restaurants = RestaurantListSerializer(source='order_num', many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'payment',
            'price',
            'firstname',
            'lastname',
            'phonenumber',
            'address',
            'comment',
            'restaurants'
        ]

    def get_status(self, status_obj):
        return status_obj.get_status_display()

    def get_payment(self, payment_obj):
        return payment_obj.get_payment_display()
