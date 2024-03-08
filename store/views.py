from django.core.paginator import Paginator

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.http import JsonResponse
from .models import *
from django.urls import reverse
from .utils import cookieCart, cartData, guestOrder

import json
import datetime


# Create your views here.


def index(request):
    data = cartData(request)
    cartItems = data['cartItems']  # Mémoriser le total d"élément cliqué par le client
    order = data['order']
    items = data['items']  # Faire afficher le total d'éléments cliqué par le client

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/index.html', context)


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']  # Mémoriser le total d"élément cliqué par le client

    products = Product.objects.all()

    paginator = Paginator(products, 6)

    page = request.GET.get('page')

    products = paginator.get_page(page)

    context = {"products": products, 'cartItems': cartItems}
    return render(request, 'store/shop.html', context)


def detail(request, slug):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']  # Faire afficher le total d'éléments cliqué par le client

    products = get_object_or_404(Product, slug=slug)

    context = {"product": products, 'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/detail.html', context)


def slide(request):
    product = Product.objects.first()
    context = {'product': product}
    return render(request, 'product/detail.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']  # Faire afficher le total d'éléments cliqué par le client

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def category(request, slug):
    pass


def detailmyid(request, myid):
    products = get_object_or_404(Product, id=myid)

    return render(request, 'store/detail.html', {"product": products})


def add_to_card(request, slug):
    pass

    return redirect(reverse("product", kwargs={"slug": slug}))


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']  # Faire afficher le total d'éléments cliqué par le client
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    """Nous voulons obtenir les données sous forme json et les envoyer au backend"""

    data = json.loads(request.body)
    productid = data['productId']
    action = data['action']
    print('action:', action)
    print('productId:', productid)
    """Nous voulons afficher ou envoyer les informations du produit selon le click du client"""

    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    print('Data: ', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total_complete = (data['form']['total'])
    total = float(total_complete.replace(",", "."))
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            telephone=data['shipping']['telephone']
        )

    return JsonResponse('Payment complete !', safe=False)


def api_get_products(request0):
    products = Product.objects.all()
    json = serializers.serialize("json", products)
    return HttpResponse(json)

