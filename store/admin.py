from django.contrib import admin
from .models import *
# Register your models here.


class AdminCustomer(admin.ModelAdmin):
    list_display = ('name', 'email')


class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_added')
    prepopulated_fields = {"slug": ("name",)}


class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'digital', 'price', 'stock', 'category', 'date_added')
    prepopulated_fields = {"slug": ("name",)}


class AdminImage(admin.ModelAdmin):
    list_display = ('name',)


class AdminOrder(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer', 'complete', 'ordered_date')


class AdminOderItem(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')


class AdminShippingAddress(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'city', 'state', 'telephone', 'date_added')


admin.site.register(Customer, AdminCustomer)

admin.site.register(Product, AdminProduct)

admin.site.register(Image, AdminImage)

admin.site.register(Category, AdminCategory)

admin.site.register(Order, AdminOrder)

admin.site.register(OrderItem, AdminOderItem)

admin.site.register(ShippingAddress, AdminShippingAddress)