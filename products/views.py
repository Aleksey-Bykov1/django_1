from django.shortcuts import render

import json


# Create your views here.


def index(request):
    return render(request, 'products/index.html')


def products(request):
    with open('db.json', 'r', encoding='utf-8') as fh:
        context = json.load(fh)
    return render(request, 'products/products.html', context)
