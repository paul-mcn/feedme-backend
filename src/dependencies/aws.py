from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
import boto3
from .env import get_environment_settings

settings = get_environment_settings()


cors_configuration = {
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["PUT", "POST", "GET", "DELETE"],
            "AllowedOrigins": ["*"],
        }
    ]
}


dynamodb_client = boto3.client(
    "dynamodb",
    endpoint_url=settings.APP_ENV == "development" and "http://localhost:8000" or None,
)

s3_client = boto3.client("s3")

# s3_client.put_bucket_cors(
#     Bucket=settings.AWS_BUCKET_NAME,
#     CORSConfiguration=cors_configuration,
# )


def init_db():
    try:
        dynamodb_client.create_table(
            TableName="MainTable",
            AttributeDefinitions=[
                {"AttributeName": "EntityType", "AttributeType": "S"},
                {"AttributeName": "EntityId", "AttributeType": "S"},
                {"AttributeName": "email", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "EntityType", "KeyType": "HASH"},
                {"AttributeName": "EntityId", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "EntityType-email-index",
                    "KeySchema": [
                        {"AttributeName": "EntityType", "KeyType": "HASH"},
                        {"AttributeName": "email", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1,
                    },
                }
            ],
        )
    except Exception as e:
        print("Couldn't create table. Here's why: %s: %s" % (type(e).__name__, e))


def get_dynamodb_client():
    return dynamodb_client


def get_main_db_table():
    return dynamodb_client.Table("MainTable")


def get_s3_client():
    return s3_client


def deserialize_list(items: list[dict]):
    items = [TypeDeserializer().deserialize(item) for item in items]
    return items


def deserialize_item(item: dict):
    item = {k: TypeDeserializer().deserialize(v) for k, v in item.items()}
    return item


def serialize_list(items: list[dict]):
    items = [TypeSerializer().serialize(item) for item in items]
    return items


def serialize_item(item):
    item = {k: TypeSerializer().serialize(v) for k, v in item.items()}
    return item
