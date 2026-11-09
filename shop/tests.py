# shop/tests.py

from django.test import TestCase
from django.urls import reverse
from shop.models import Category, Product

class ShopModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category = self.category,
            name = 'Laptop',
            slug = 'laptop',
            price = 999.99,
            available = True
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Electronics')
        self.assertEqual(self.category.get_absolute_url(), '/electronics/')

    def test_product_creation(self):
        self.assertEqual(str(self.product), 'Laptop')
        self.assertEqual(self.product.price, 999.99)

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertTemplateUsed(response, 'shop/product/list.html')