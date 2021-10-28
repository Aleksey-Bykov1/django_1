from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from products.models import ProductsCategory, Product
from users.models import User


class TestMainSmokeTest(TestCase):
    status_code_success = 200
    status_code_render = 302
    username = 'django'
    email = 'django@mail.ru'
    password = 'geekshop'

    new_user_data = {
        'username': 'test_django',
        'first_name': 'Django',
        'last_name': 'Django2',
        'password1': 'DjAnG0',
        'password2': 'DjAnG0',
        'email': 'dj_super@bk.ru'
    }

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, self.status_code_render)

    def test_register(self):
        response = self.client.post('/users/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.status_code_render)
        new_user = User.objects.get(username=self.new_user_data['username'])

        activation_url = f'{settings.DOMAIN_NAME}/users/verify/{self.new_user_data["email"]}/{new_user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

