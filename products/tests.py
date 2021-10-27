from django.test import TestCase
from django.test.client import Client

from products.models import ProductsCategory, Product


class TestMainSmokeTest(TestCase):

    def setUp(self):
        category = ProductsCategory.objects.create(name='test_cat')
        Product.objects.create(category=category, name='prod_test', price=100)

        self.client = Client()

    def test_product_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_products_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/detail/{product_item.pk}/')
            self.assertEqual(response.status_code, 200)

    def test_products_basket(self):
        response = self.client.get(f'/users/profile/')
        self.assertEqual(response.status_code, 302)

