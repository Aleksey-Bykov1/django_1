from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm
from users.models import User


# Create your views here.


def index(request):
    return render(request, 'admins/admin.html')


@user_passes_test(lambda u: u.is_superuser)
def admin_user(request):
    context = {
        'title': 'GeekShop - Список пользователей',
        'users': User.objects.all()
    }
    return render(request, 'admins/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_user_create(request):
        if request.method == 'POST':
            form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Пользователь создан')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = UserAdminRegisterForm()
        context = {
            'title': 'GeekShop - Создание пользователя',
            'form': form
        }

        return render(request, 'admins/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_user_update(request, id):
    user_select = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserAdminProfileForm(data=request.POST, instance=user_select, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены успешно')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = UserAdminProfileForm(instance=user_select)
    context = {
                'title': 'GeekShop - Редактирование пользователя',
                'form': form,
                'user_select': user_select
            }
    return render(request, 'admins/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_user_delete(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admins:admin_user'))
