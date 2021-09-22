from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm
from users.models import User
from products.models import ProductsCategory


# Create your views here.


def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)

# @user_passes_test(lambda u: u.is_superuser)
# def admin_user(request):
#     context = {
#         'title': 'GeekShop - Список пользователей',
#         'users': User.objects.all()
#     }
#     return render(request, 'admins/admin-users-read.html', context)






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


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories_list = ProductsCategory.objects.all()
    context = {
        'title': 'Админка - категории',
        'objects': categories_list
    }

    return render(request, 'admins/categories.html', context)


def category_create(request):
    pass


def category_update(request, id):
    pass


def category_delete(request, id):
    pass

