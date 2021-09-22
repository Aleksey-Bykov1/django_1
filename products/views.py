from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import json
from .models import Product, ProductsCategory


# Create your views here.


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)


def products(request, id=None):
    title = 'Каталог'
    category = ProductsCategory.objects.all()
    if id != None:
        products_filter = Product.objects.filter(category_id=id)
    else:
        products_filter = Product.objects.all()

    context = {'title': title, 'products': products_filter, 'category': category}
    return render(request, 'products/products.html', context)
