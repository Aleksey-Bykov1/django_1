from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from users.models import User


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                              'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                              'placeholder': 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')

    # def clean_image(self):
    #     data = self.cleaned_data['image']
    #     if data.size > 1024:
    #         raise forms.ValidationError('Слишком большой файл')
    #
    #     return data

    def clean_first_name(self):
        text = self.cleaned_data['first_name']
        if len(text) > 24:
            raise forms.ValidationError('Не больше 24 символов')

        return text


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                             'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control py-4',
                                                                 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('password', 'username')


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                             'placeholder': 'Введите логин'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4',
                                                           'placeholder': 'Введите электронную почту'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                              'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                              'placeholder': 'Введите фамилию'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control py-4',
                                                                  'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control py-4',
                                                                  'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')