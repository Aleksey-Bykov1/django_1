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
from .views import index, UserListView, admin_user_create, admin_user_update, admin_user_delete, categories, category_create, category_delete, category_update


app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_user'),
    path('user_create/', admin_user_create, name='admin_user_create'),
    path('user_update/<int:id>', admin_user_update, name='admin_user_update'),
    path('user_delete/<int:id>', admin_user_delete, name='admin_user_delete'),

    path('categories/create/', category_create, name='category_create'),
    path('categories/read/', categories, name='categories'),
    path('categories/update/<int:id>', category_update, name='category_update'),
    path('categories/delete/<int:id>', category_delete, name='category_delete'),
]
