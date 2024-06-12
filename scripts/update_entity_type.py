import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

# Configuration
dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
table_name = "MainTable"
old_entity_type = "account#meals"
new_entity_type = "all#meals"


def serialize_item(item):
    item = {k: TypeSerializer().serialize(v) for k, v in item.items()}
    return item


def deserialize_item(item: dict):
    item = {k: TypeDeserializer().deserialize(v) for k, v in item.items()}
    return item


def update_entity_type(old_entity_type, new_entity_type):
    # Step 1: Query items with the old entity type
    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression="EntityType = :entityType",
        ExpressionAttributeValues={":entityType": {"S": old_entity_type}},
    )

    items = response.get("Items", [])

    for serialized_item in items:
        item = deserialize_item(serialized_item)

        entity_id = item["EntityId"]

        # Step 2: Update the EntityType in the item
        item["EntityType"] = new_entity_type
        new_item = serialize_item(item)

        # Step 3: Put the modified item back into the table
        dynamodb.put_item(TableName=table_name, Item=new_item)

        # Step 4: Delete the old item
        dynamodb.delete_item(
            TableName=table_name,
            Key={"EntityId": {"S": entity_id}, "EntityType": {"S": old_entity_type}},
        )

    print(
        f"EntityType updated for all items from {old_entity_type} to {new_entity_type}"
    )


# Run the update function
update_entity_type(old_entity_type, new_entity_type)
