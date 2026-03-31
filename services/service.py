from datetime import datetime, timezone
from .repository import ShippingRepository
from .publisher import ShippingPublisher


class ShippingService:
    SHIPPING_CREATED = 'created';
    SHIPPING_IN_PROGRESS = 'in progress'
    SHIPPING_COMPLETED = 'completed';
    SHIPPING_FAILED = 'failed'

    def __init__(self, repository, publisher):
        self.repository = repository
        self.publisher = publisher

    @staticmethod
    def list_available_shipping_type():
        return ['Нова Пошта', 'Укр Пошта', 'Meest Express', 'Самовивіз']

    def create_shipping(self, shipping_type, product_ids, order_id, due_date):
        if shipping_type not in self.list_available_shipping_type(): raise ValueError("Shipping type is not available")
        if due_date <= datetime.now(timezone.utc): raise ValueError("Due date must be in future")

        ship_id = self.repository.create_shipping(shipping_type, product_ids, order_id, self.SHIPPING_CREATED, due_date)
        self.publisher.send_new_shipping(ship_id)
        self.repository.update_shipping_status(ship_id, self.SHIPPING_IN_PROGRESS)
        return ship_id

    def check_status(self, shipping_id):
        ship = self.repository.get_shipping(shipping_id)
        return ship['shipping_status'] if ship else None

    def process_shipping_batch(self):
        ids = self.publisher.poll_shipping()
        results = []
        for sid in ids:
            ship = self.repository.get_shipping(sid)
            if datetime.fromisoformat(ship['due_date']) < datetime.now(timezone.utc):
                self.repository.update_shipping_status(sid, self.SHIPPING_FAILED)
            else:
                self.repository.update_shipping_status(sid, self.SHIPPING_COMPLETED)
            results.append(sid)
        return results