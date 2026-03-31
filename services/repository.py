from uuid import uuid4
from datetime import datetime, timezone
from .config import SHIPPING_TABLE_NAME
from .db import get_dynamodb_resource

class ShippingRepository:
    def __init__(self):
        self.db = get_dynamodb_resource()
        self.table = self.db.Table(SHIPPING_TABLE_NAME)

    def get_shipping(self, shipping_id):
        return self.table.get_item(Key={"shipping_id": shipping_id}).get("Item")

    def create_shipping(self, shipping_type, product_ids, order_id, status, due_date):
        shipping_id = str(uuid4())
        item = {
            "shipping_id": shipping_id, "shipping_type": shipping_type, "order_id": order_id,
            "product_ids": ",".join(product_ids), "shipping_status": status,
            "created_date": datetime.now(timezone.utc).isoformat(),
            "due_date": due_date.replace(tzinfo=timezone.utc).isoformat()
        }
        self.table.put_item(Item=item)
        return shipping_id

    def update_shipping_status(self, shipping_id, status):
        self.table.update_item(
            Key={'shipping_id': shipping_id},
            UpdateExpression='SET shipping_status = :val',
            ExpressionAttributeValues={':val': status}
        )