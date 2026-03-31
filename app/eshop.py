import uuid
from dataclasses import dataclass

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

    def __eq__(self, other):
        if not isinstance(other, Product): return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

class ShoppingCart:
    def __init__(self):
        self.products = dict()

    def contains_product(self, product):
        return product in self.products

    def add_product(self, product: Product, amount: int):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if not product.is_available(amount):
            raise ValueError(f"Product {product} has only {product.available_amount} items")
        self.products[product] = self.products.get(product, 0) + amount

    def remove_product(self, product):
        if product in self.products:
            del self.products[product]

    def calculate_total(self):
        return sum([p.price * count for p, count in self.products.items()])

    def submit_cart_order(self):
        product_ids = []
        for product, count in self.products.items():
            product.buy(count)
            product_ids.append(str(product))
        self.products.clear()
        return product_ids

class Order:
    def __init__(self, cart, shipping_service=None, order_id=None):
        self.cart = cart
        self.shipping_service = shipping_service
        self.order_id = order_id if order_id else str(uuid.uuid4())

    def place_order(self, shipping_type="Самовивіз", due_date=None):
        product_ids = self.cart.submit_cart_order()
        if self.shipping_service:
            return self.shipping_service.create_shipping(shipping_type, product_ids, self.order_id, due_date)
        return "order_placed_locally"

@dataclass
class Shipment:
    shipping_id: str
    shipping_service: any
    def check_shipping_status(self):
        return self.shipping_service.check_status(self.shipping_id)