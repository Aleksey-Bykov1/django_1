from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from django.views.generic import FormView, UpdateView

from .models import User


class LoginListView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = 'index'

    def get(self, request, *args, **kwargs):
        sup = super(LoginListView, self).get(request, *args, **kwargs)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        return sup

    def get_success_url(self):
        return reverse('products:index')

    def get_context_data(self, **kwargs):
        context = super(LoginListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Авторизация'
        return context

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('products:index'))
#     else:
#         form = UserLoginForm()
#     context = {
#             'title': 'GeekShop - Авторизация',
#             'form': form
#         }
#
#     return render(request, 'users/login.html', context)


class RegisterListView(FormView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super(RegisterListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.success(request, 'Вы успешно зарегистрировались!')
                return redirect(self.success_url)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def send_verify_link(user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} на портале GeekShop \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    @staticmethod
    def verify(request, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(request, user)
            return render(request, 'users/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             if send_verify_link(user):
#                 messages.success(request, 'Вы успешно зарегистрировались')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {
#             'title': 'GeekShop - Регистрация',
#             'form': form
#         }
#
#     return render(request, 'users/register.html', context)


class ProfileFormView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/profile.html'
    form_class_second = UserProfileEditForm
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Профиль'
        context['profile_form'] = self.form_class_second(instance=self.request.user.userprofile)

        return

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        edit_form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

        return render(request, self.template_name, {
            'form': edit_form,
            'profile_form': profile_form,
        })

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        edit_form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=user.userprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {
            'form': edit_form,
            'profile_form': profile_form,
        })


# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
#         if form.is_valid() and profile_form.is_valid():
#             form.save()
#             messages.success(request, 'Изменения сохранены успешно')

#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#         profile_form = UserProfileEditForm(instance=request.user.userprofile)
#     context = {
#                 'title': 'GeekShop - Профиль',
#                 'form': form,
#                 'profile_form': profile_form
#             }
#
#     return render(request, 'users/profile.html', context)


class Logout(LogoutView):
    template_name = 'products/index.html'

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
