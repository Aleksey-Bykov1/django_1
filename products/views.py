from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
from .models import Product, ProductsCategory


# Create your views here.


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)


def products(request, id=None, page=1):
    title = 'Каталог'
    category = ProductsCategory.objects.all()
    if id != None:
        products_filter = Product.objects.filter(category_id=id)
    else:
        products_filter = Product.objects.all()

    paginator = Paginator(products_filter, per_page=2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {'title': title, 'products': products_paginator, 'category': category}
    return render(request, 'products/products.html', context)
