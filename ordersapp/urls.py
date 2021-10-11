"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from baskets.views import basket_add, basket_remove, baskets_edit

from .views import OrderRead, OrderList, OrderDelete, OrderUpdate, OrderCreate, order_forming_complete

app_name = 'ordersapp'

urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('read/<int:pk>', OrderRead.as_view(), name='read'),
    path('update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('delete/<int:pk>', OrderDelete.as_view(), name='delete'),
    path('forming-complete/<int:pk>', order_forming_complete, name='forming_complete'),
]
