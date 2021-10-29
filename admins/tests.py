from django.test import TestCase
from django.test.client import Client

from users.models import User


class TestMainSmokeTest(TestCase):
    status_code_success = 200
    status_code_render = 302
    username = 'django'
    email = 'django@mail.ru'
    password = 'geekshop'

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    def test_admin_users_read(self):
        response = self.client.get('/admins/users/')
        self.client.login(username=self.username, password=self.password)
        self.assertEqual(response.status_code, self.status_code_render)

    def test_admin_user_create(self):
        response = self.client.get('/admins/category/')
        self.client.login(username=self.username, password=self.password)
        self.assertEqual(response.status_code, self.status_code_render)
