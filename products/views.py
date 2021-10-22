from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from .models import Product, ProductsCategory
from django.conf import settings
from django.core.cache import cache

# Create your views here.


def get_links_category():
    if settings.LOW_CACHE:
        key = 'links_category'
        links_category = cache.get(key)
        if links_category is None:
            links_category = ProductsCategory.objects.filter(is_active=True)
            cache.set(key, links_category)
        return links_category
    else:
        return ProductsCategory.objects.filter(is_active=True)


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_links_product():
    if settings.LOW_CACHE:
        key = 'links_product'
        links_product = cache.get(key)
        if links_product is None:
            links_product = Product.objects.filter(is_active=True).select_related()
            cache.set(key, links_product)
        return links_product
    else:
        return Product.objects.filter(is_active=True).select_related()


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Каталог'
        context['category'] = get_links_category()
        return context

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(ProductListView, self).get_queryset()
        if category_id := self.kwargs.get('id'):
            qs = qs.filter(category_id=category_id)
        return qs


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


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['product'] = get_product(self.kwargs.get('pk'))
        context['categories'] = ProductsCategory.objects.all()
        return context
