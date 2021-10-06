from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Product, ProductsCategory


# Create your views here.


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)


class ProductListView(ListView, Paginator):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Каталог'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)


# def products(request, id=None, page=1):
#     title = 'Каталог'
#     category = ProductsCategory.objects.all()
#     if id != None:
#         products_filter = Product.objects.filter(category_id=id)
#     else:
#         products_filter = Product.objects.all()
#
#     paginator = Paginator(products_filter, per_page=2)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#
#     context = {'title': title, 'products': products_paginator, 'category': category}
#     return render(request, 'products/products.html', context)
