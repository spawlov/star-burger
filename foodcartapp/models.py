from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def get_order_list(self):
        orders = (Order.objects
                  .filter(status__in=['WAITING', 'PROCESSED'])
                  .annotate(price=Sum(
                        F('orders__price') * F('orders__quantity')
                        ),
                    )
                  .order_by('-status', 'pk')
                  )
        order_items = {}
        for order in orders:
            order_items[order.pk] = {'rests': []}
            order_items[order.pk]['status'] = order.get_status_display()
            order_items[order.pk]['payment'] = order.get_payment_display()
            order_items[order.pk]['price'] = order.price
            order_items[order.pk]['firstname'] = order.firstname
            order_items[order.pk]['lastname'] = order.lastname
            order_items[order.pk]['phonenumber'] = order.phonenumber
            order_items[order.pk]['address'] = order.address
            order_items[order.pk]['comment'] = order.comment

            order_items[order.pk]['rests'] = list(
                RestaurantOrder.objects
                .select_related()
                .filter(order=order)
                .values_list('restaurant__name', flat=True)
            )

        return order_items


class Order(models.Model):
    status = (
        ('WAITING', 'Необработан'),
        ('PROCESSED', 'Готовится'),
        ('COMPLETED', 'Завершен'),
    )
    payment = (
        ('CARD', 'Электронно'),
        ('CASH', 'Наличные'),
    )
    status = models.CharField(
        max_length=9,
        choices=status,
        default='WAITING',
        verbose_name='статус заказа',
    )
    payment = models.CharField(
        max_length=4,
        choices=payment,
        default='CASH',
        verbose_name='способ оплаты',
    )
    firstname = models.CharField(
        max_length=20,
        verbose_name='имя',
    )
    lastname = models.CharField(
        max_length=20,
        verbose_name='фамилия',
    )
    phonenumber = PhoneNumberField(
        region='RU',
        verbose_name='телефон',
    )
    address = models.CharField(
        max_length=128,
        verbose_name='адрес доставки'
    )
    comment = models.TextField(
        max_length=250,
        blank=True,
        verbose_name='комментарий',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создан',
    )
    called = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='звонок клиенту',
    )
    completed = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='доставлен',
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        indexes = [
            models.Index(fields=[
                'phonenumber',
                'firstname',
                'lastname',
                'address',
                'status',
                'called',
                'completed',
                'payment'
            ]
            )
        ]

    def __str__(self):
        return f'Заказ №{self.pk}'


class ProductOrder(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='заказ',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='наименование',
    )
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='количество'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0.00,
        verbose_name='цена',
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.product.name


class RestaurantOrder(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='заказ'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='restaurants',
        on_delete=models.PROTECT,
        verbose_name='ресторан',
    )
    distance = models.FloatField(
        verbose_name='расстояние'
    )

    class Meta:
        verbose_name = 'ресторан готовящий заказ'
        verbose_name_plural = 'рестораны готовящие заказ'

    def __str__(self):
        return self.restaurant.name
