from django.core.management.base import BaseCommand
from products.models import Product
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.filter(Q(category__name='Обувь') | Q(category__name='Подарки'))
        print(products)
