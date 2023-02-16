import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, ProductOrder


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
        try:
            products = order_data['products']
        except KeyError:
            return Response(
                {'error': 'products: Обязательное поле.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if products is None:
                return Response(
                    {'error': 'products: Это поле не может быть пустым.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not isinstance(products, list):
                return Response(
                    {'error': 'products: Ожидался list со значениями'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not len(products):
                return Response(
                    {'error': 'products: Этот список не может быть пустым.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order = Order.objects.create(
                first_name=order_data['firstname'],
                last_name=order_data['lastname'],
                phone=order_data['phonenumber'],
                address=order_data['address']
            )

            for position in order_data['products']:
                product = Product.objects.get(pk=position['product'])
                ProductOrder.objects.create(
                    order=order,
                    product=product,
                    quantity=position['quantity']
                )

    return Response({}, status=status.HTTP_201_CREATED)
