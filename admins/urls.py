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

import admins.views
from .views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView, \
    CategoriesListView, CategoriesCreateView, category_delete, category_update


app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_user'),
    path('user_create/', UserCreateView.as_view(), name='admin_user_create'),
    path('user_update/<int:pk>', UserUpdateView.as_view(), name='admin_user_update'),
    path('user_delete/<int:pk>', UserDeleteView.as_view(), name='admin_user_delete'),

    path('categories/create/', CategoriesCreateView.as_view(), name='category_create'),
    path('categories/read/', CategoriesListView.as_view(), name='categories'),
    path('categories/update/<int:id>', category_update, name='category_update'),
    path('categories/delete/<int:id>', category_delete, name='category_delete'),
]
