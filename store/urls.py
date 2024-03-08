from django.urls import path, include

from . import views

app_name = 'store'

urlpatterns = [
    path('index', views.index, name="index"),
    path('', views.store, name="shop"),
    path('detail', views.detail, name="detail"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('api/GetProducts', views.api_get_products),

]
