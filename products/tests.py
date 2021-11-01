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

    # def test_products_product(self):
    #     for product_item in Product.objects.all():
    #         response = self.client.get(f'/products/detail/{product_item.pk}/')
    #         self.assertEqual(response.status_code, 200)

    def test_products_basket(self):
        response = self.client.get(f'/users/profile/')
        self.assertEqual(response.status_code, 302)


class ProductTestCase(TestCase):
    def setUp(self):
        category = ProductsCategory.objects.create(name='Clothes')
        self.product_1 = Product.objects.create(name='Shirt', category=category, price=2341.6, quantity=30)
        self.product_2 = Product.objects.create(name='Pans', category=category, price=1245.8, quantity=43)
        self.product_3 = Product.objects.create(name='Jacket', category=category, price=14576.34, quantity=22)

    def test_product_get(self):
        product_1 = Product.objects.get(name='Shirt')
        product_2 = Product.objects.get(name='Pans')
        product_3 = Product.objects.get(name='Jacket')
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)
        self.assertEqual(product_3, self.product_3)

    def test_product_print(self):
        product_1 = Product.objects.get(name='Shirt')
        product_2 = Product.objects.get(name='Pans')
        product_3 = Product.objects.get(name='Jacket')
        self.assertEqual(str(product_1), 'Shirt (Clothes)')
        self.assertEqual(str(product_2), 'Pans (Clothes)')
        self.assertEqual(str(product_3), 'Jacket (Clothes)')

    # def test_product_get_items(self):
    #     product_1 = Product.objects.get(name='Shirt')
    #     product_2 = Product.objects.get(name='Pans')
    #     product_3 = Product.objects.get(name='Jacket')
    #     products = product_1.get_items()
    #     self.assertEqual(list(products), [product_1, product_3])
