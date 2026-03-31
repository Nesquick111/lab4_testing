import pytest
import boto3
from services.config import *
from services.db import get_dynamodb_resource


@pytest.fixture(scope="session", autouse=True)
def setup_localstack_resources():
    params = {'aws_access_key_id': 'test', 'aws_secret_access_key': 'test', 'region_name': AWS_REGION}
    db_client = boto3.client("dynamodb", endpoint_url=AWS_ENDPOINT_URL, **params)

    tables = db_client.list_tables()["TableNames"]
    if SHIPPING_TABLE_NAME not in tables:
        db_client.create_table(
            TableName=SHIPPING_TABLE_NAME,
            KeySchema=[{"AttributeName": "shipping_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "shipping_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
    db_client.get_waiter("table_exists").wait(TableName=SHIPPING_TABLE_NAME)

    sqs = boto3.client("sqs", endpoint_url=AWS_ENDPOINT_URL, **params)
    sqs.create_queue(QueueName=SHIPPING_QUEUE)
    yield


@pytest.fixture
def dynamo_resource():
    return get_dynamodb_resource()