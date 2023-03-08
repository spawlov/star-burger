from django.core.validators import MinValueValidator
from django.db import models
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
    def get_order_price(self):

        orders_with_price = (Order.objects
                             .prefetch_related('order_num__restaurant')
                             .filter(status__in=['WAITING', 'PROCESS'])
                             .annotate(price=Sum(
                                F('order_no__price') * F('order_no__quantity')
                                )
                                )
                             .order_by('-status', 'pk')
                             )
        return orders_with_price


class Order(models.Model):
    status = (
        ('WAITING', 'Необработан'),
        ('PROCESS', 'Готовится'),
        ('COMPLETED', 'Завершен'),
    )
    payment = (
        ('CARD', 'Электронно'),
        ('CASH', 'Наличные'),
    )
    status = models.CharField(
        max_length=10,
        choices=status,
        default='WAITING',
        db_index=True,
        verbose_name='статус заказа',
    )
    payment = models.CharField(
        max_length=4,
        choices=payment,
        blank=True,
        db_index=True,
        verbose_name='способ оплаты',
    )
    firstname = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='имя',
    )
    lastname = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='фамилия',
    )
    phonenumber = PhoneNumberField(
        region='RU',
        db_index=True,
        verbose_name='телефон',
    )
    address = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name='адрес доставки'
    )
    comment = models.TextField(
        max_length=250,
        blank=True,
        verbose_name='комментарий',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='создан',
    )
    called_at = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        verbose_name='звонок клиенту',
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        verbose_name='доставлен',
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ №{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_no',
        blank=True,
        verbose_name='заказ',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='наименование',
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(100)],
        default=100.00,
        verbose_name='цена',
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.product.name}, {self.price}руб.'


class RestaurantOrder(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_num',
        verbose_name='заказ'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='restaurants',
        on_delete=models.PROTECT,
        verbose_name='ресторан',
    )
    distance = models.FloatField(
        validators=[MinValueValidator(0)],
        default=100,
        verbose_name='расстояние'
    )

    class Meta:
        verbose_name = 'ресторан готовящий заказ'
        verbose_name_plural = 'рестораны готовящие заказ'
        ordering = ['distance']

    def __str__(self):
        return self.restaurant.name
