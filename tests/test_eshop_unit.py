import unittest
from unittest.mock import MagicMock
from app.eshop import Product, ShoppingCart, Order # ЗМІНЕНО ІМПОРТ

class TestEshopUnit(unittest.TestCase):
    def setUp(self):
        self.product = Product(name='Test', price=100.0, available_amount=10)
        self.cart = ShoppingCart()

    def test_add_available_amount(self):
        self.cart.add_product(self.product, 5)
        self.assertTrue(self.cart.contains_product(self.product))

    def test_calculate_total(self):
        self.cart.add_product(self.product, 2)
        self.assertEqual(self.cart.calculate_total(), 200.0)

    def test_buy_decreases_stock(self):
        self.product.buy(3)
        self.assertEqual(self.product.available_amount, 7)

    def test_negative_amount_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.add_product(self.product, -5)