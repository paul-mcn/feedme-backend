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
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME,
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME,
)

# s3_client.put_bucket_cors(
#     Bucket=settings.AWS_BUCKET_NAME,
#     CORSConfiguration=cors_configuration,
# )


def get_dynamodb_client():
    return dynamodb_client


def get_main_db_table():
    return dynamodb_client.Table("MainTable")


def get_s3_client():
    return s3_client


def deserialize_item(item):
    item = {k: TypeDeserializer().deserialize(v) for k, v in item.items()}
    return item


def serialize_item(item):
    item = {k: TypeSerializer().serialize(v) for k, v in item.items()}
    return item
