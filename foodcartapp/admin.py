import datetime

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.templatetags.static import static
from django.utils.html import format_html

from .models import Order
from .models import Product
from .models import ProductCategory
from .models import ProductOrder
from .models import Restaurant
from .models import RestaurantMenuItem
from .models import RestaurantOrder
from .services import calc_distance


class RestaurantMenuItemInline(admin.TabularInline):
    model = RestaurantMenuItem
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'address',
        'contact_phone',
    ]
    list_display = [
        'name',
        'address',
        'contact_phone',
    ]
    inlines = [
        RestaurantMenuItemInline
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'get_image_list_preview',
        'name',
        'category',
        'price',
    ]
    list_display_links = [
        'name',
    ]
    list_filter = [
        'category',
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'name',
        'category__name',
    ]

    inlines = [
        RestaurantMenuItemInline
    ]
    fieldsets = (
        ('Общее', {
            'fields': [
                'name',
                'category',
                'image',
                'get_image_preview',
                'price',
            ]
        }),
        ('Подробно', {
            'fields': [
                'special_status',
                'description',
            ],
            'classes': [
                'wide'
            ],
        }),
    )

    readonly_fields = [
        'get_image_preview',
    ]

    class Media:
        css = {
            "all": (
                static("admin/foodcartapp.css")
            )
        }

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>',
                           url=obj.image.url)

    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:foodcartapp_product_change', args=(obj.id,))
        return format_html(
            '<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/></a>',
            edit_url=edit_url, src=obj.image.url)

    get_image_list_preview.short_description = 'превью'


@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    pass


class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 0


class RestaurantOrderInline(admin.TabularInline):
    model = RestaurantOrder
    readonly_fields = ['distance']
    ordering = ['distance']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        'id',
        'created',
        'firstname',
        'lastname',
        'phonenumber',
        'address',
        'status'
    ]
    list_display_links = [
        'created',
        'firstname',
        'lastname',
        'phonenumber',
        'address',
        'status'
    ]
    list_filter = ['status']
    readonly_fields = ['created', 'called', 'completed']

    inlines = [
        ProductOrderInline,
        RestaurantOrderInline
    ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
            if obj.__class__.__name__ == 'RestaurantOrder':
                if RestaurantOrder.objects.filter(
                    order=obj.order
                ).count() == 1:
                    Order.objects.filter(pk=obj.order_id).update(
                        status='PROCESSED',
                        called=datetime.datetime.now(),
                    )
        for instance in instances:
            if instance.__class__.__name__ == 'ProductOrder':
                if not instance.price:
                    instance.price = (
                        Product.objects
                        .get(pk=instance.product_id)
                        .price
                    )
                instance.save()
            elif instance.__class__.__name__ == 'RestaurantOrder':
                if not instance.distance:
                    distance = calc_distance(
                        instance.restaurant.address,
                        instance.order.address
                    )
                    instance.distance = round(distance, 2)
                instance.save()
                if RestaurantOrder.objects.filter(
                    order=instance.order
                ).count() == 1:
                    Order.objects.filter(pk=instance.order_id).update(
                        status='PROCESSED',
                        called=datetime.datetime.now(),
                    )
        formset.save()

    def response_post_save_change(self, request, obj):
        result = super().response_post_save_change(request, obj)
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return result
