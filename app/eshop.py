import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from services import ShippingService

class Product:
    def __init__(self, name, price, available_amount):
        self.name = name
        self.price = price
        self.available_amount = available_amount
    def is_available(self, requested_amount):
        return self.available_amount >= requested_amount
    def buy(self, requested_amount):
        if not self.is_available(requested_amount):
            raise ValueError("Not enough stock")
        self.available_amount -= requested_amount
    def __str__(self):
        return self.name

class ShoppingCart:
    def __init__(self):
        self.products = dict()
    def add_product(self, product: Product, amount: int):
        if amount <= 0: raise ValueError("Amount must be positive")
        if not product.is_available(amount): raise ValueError("Not enough stock")
        self.products[product] = self.products.get(product, 0) + amount
    def submit_cart_order(self):
        product_ids = []
        for product, count in self.products.items():
            product.buy(count)
            product_ids.append(str(product))
        self.products.clear()
        return product_ids

@dataclass
class Order:
    cart: ShoppingCart
    shipping_service: ShippingService
    order_id: str = None
    def __post_init__(self):
        if not self.order_id: self.order_id = str(uuid.uuid4())
    def place_order(self, shipping_type, due_date: datetime = None):
        if not due_date:
            due_date = datetime.now(timezone.utc) + timedelta(seconds=3)
        product_ids = self.cart.submit_cart_order()
        return self.shipping_service.create_shipping(shipping_type, product_ids, self.order_id, due_date)

@dataclass
class Shipment:
    shipping_id: str
    shipping_service: ShippingService
    def check_shipping_status(self):
        return self.shipping_service.check_status(self.shipping_id)