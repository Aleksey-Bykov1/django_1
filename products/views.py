from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import json
from .models import Product, ProductsCategory


# Create your views here.


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)


def products(request):
    title = 'Каталог'
    product = Product.objects.all()
    category = ProductsCategory.objects.all()
    context = {'title': title, 'products': product, 'category': category}
    return render(request, 'products/products.html', context)
