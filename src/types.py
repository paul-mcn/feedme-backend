from typing import TypedDict


class DynamoDBQueryResponse(TypedDict):
    Items: list
    Count: int
