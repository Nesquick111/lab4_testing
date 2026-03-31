import pytest
import uuid
import random
from datetime import datetime, timedelta, timezone
from app.eshop import Product, ShoppingCart, Order
from services.service import ShippingService
from services.repository import ShippingRepository
from services.publisher import ShippingPublisher


def test_repository_create_and_get(dynamo_resource):
    repo = ShippingRepository()
    order_id = str(uuid.uuid4())
    ship_id = repo.create_shipping("Нова Пошта", ["Prod1"], order_id, "created",
                                   datetime.now(timezone.utc) + timedelta(days=1))

    data = repo.get_shipping(ship_id)
    assert data["order_id"] == order_id
    assert data["shipping_status"] == "created"


def test_repository_update_status(dynamo_resource):
    repo = ShippingRepository()
    ship_id = repo.create_shipping("Укр Пошта", ["Prod2"], "ord_123", "created",
                                   datetime.now(timezone.utc) + timedelta(days=1))
    repo.update_shipping_status(ship_id, "in progress")

    data = repo.get_shipping(ship_id)
    assert data["shipping_status"] == "in progress"


def test_publisher_send_and_poll():
    pub = ShippingPublisher()
    ship_id = "ship_" + str(uuid.uuid4())
    pub.send_new_shipping(ship_id)

    messages = pub.poll_shipping(batch_size=1)
    assert ship_id in messages


def test_service_create_shipping_flow(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    due_date = datetime.now(timezone.utc) + timedelta(hours=5)
    ship_id = service.create_shipping("Meest Express", ["item1"], "order_999", due_date)

    assert ShippingRepository().get_shipping(ship_id) is not None
    assert ship_id in ShippingPublisher().poll_shipping()


def test_service_invalid_type():
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    with pytest.raises(ValueError, match="Shipping type is not available"):
        service.create_shipping("Teleport", ["id"], "ord", datetime.now(timezone.utc))


def test_service_invalid_date():
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    past_date = datetime.now(timezone.utc) - timedelta(days=1)
    with pytest.raises(ValueError, match="Due date must be in future"):
        service.create_shipping("Нова Пошта", ["id"], "ord", past_date)


def test_order_place_integration(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product("Phone", 1000, 5), 1)
    order = Order(cart, service)

    ship_id = order.place_order("Нова Пошта")
    assert ship_id is not None
    assert service.check_status(ship_id) == "in progress"


def test_process_shipping_batch(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    pub = ShippingPublisher()
    id1 = service.create_shipping("Самовивіз", ["p1"], "o1", datetime.now(timezone.utc) + timedelta(days=1))
    id2 = service.create_shipping("Самовивіз", ["p2"], "o2", datetime.now(timezone.utc) + timedelta(days=1))

    results = service.process_shipping_batch()
    assert len(results) >= 2


def test_process_expired_shipping(dynamo_resource):
    repo = ShippingRepository()
    pub = ShippingPublisher()
    service = ShippingService(repo, pub)

    due_date = datetime.now(timezone.utc) + timedelta(seconds=1)
    ship_id = repo.create_shipping("Нова Пошта", ["p"], "o", "created", due_date)
    pub.send_new_shipping(ship_id)

    import time
    time.sleep(2)

    service.process_shipping_batch()
    assert service.check_status(ship_id) == "failed"


from app.eshop import Shipment


def test_shipment_status_check(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    ship_id = service.create_shipping("Укр Пошта", ["item"], "ord", datetime.now(timezone.utc) + timedelta(days=1))
    shipment = Shipment(ship_id, service)

    assert shipment.check_shipping_status() == "in progress"