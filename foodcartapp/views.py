from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, ProductOrder, Order, RestaurantMenuItem, \
    RestaurantOrder
from .serializers import OrderSerializer, OrderSerializerResponse
from .services import calc_distance


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):

    if request.method == 'POST':
        order_data = request.data
        serializer = OrderSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            order = Order.objects.create(
                firstname=serializer.validated_data['firstname'],
                lastname=serializer.validated_data['lastname'],
                phonenumber=serializer.validated_data['phonenumber'],
                address=serializer.validated_data['address']
            )

            product_list = serializer.validated_data['products']
            order_products = [
                ProductOrder(
                    order=order,
                    price=fields['product'].price,
                    **fields
                ) for fields in product_list
            ]
            products = ProductOrder.objects.bulk_create(order_products)

            for product in products:
                rests = RestaurantMenuItem.objects.filter(
                        product_id=product.product_id, availability=True
                        )
                result_rests = []
                if not result_rests:
                    result_rests = rests
                set_rests = set(result_rests).intersection(set(rests))
                if not set_rests:
                    break
                else:
                    result_rests = rests
            for restaurant in result_rests:
                distance = calc_distance(
                    restaurant.restaurant.address,
                    order.address
                )
                RestaurantOrder.objects.create(
                    order=order,
                    restaurant=restaurant.restaurant,
                    distance=round(distance, 2)
                )

            created_order = OrderSerializerResponse(order)

        return Response(created_order.data, status=status.HTTP_201_CREATED)
