from boto3.dynamodb.types import TypeDeserializer
import boto3

def deserialize_item(item):
    item = {k: TypeDeserializer().deserialize(v) for k, v in item.items()}
    return item


dynamodb_client = boto3.client("dynamodb")
