import json
import os

import boto3

dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]


def handler(event, context):
    file_id = event["path"].replace('/files/', "")

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={"file_id": {"S": file_id}}).get("Item")

    if not result:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "File not found"
            })
        }

    try:
        text_blocks = result.get('text', {}).get('SS', [])

    except AttributeError:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "File not found"
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "file_id": file_id,
                "text": text_blocks,
            }
        )
    }
