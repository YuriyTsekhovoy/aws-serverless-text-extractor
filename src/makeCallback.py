import os
import json
import urllib3
import boto3

dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]


def handler(event, context):

    file_id = event["Records"][0]["dynamodb"]["Keys"]["file_id"]["S"]

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={"file_id": {"S": file_id}}).get("Item")

    if not result:
        return {
            "statusCode": 400, "body": json.dumps({
                "error": "No record with specified file_id"
            })
        }

    text_blocks = result.get('text', {}).get('SS', [])

    if not text_blocks:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No text blocks found for specified file ID'})
        }

    callback_url = result.get('callback_url', {}).get('S', '').strip()
    if not callback_url:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Callback URL not provided'})
        }

    data = {'fileId': file_id, 'text': text_blocks}

    http = urllib3.PoolManager()
    response = http.request(
        'POST',
        callback_url,
        body=json.dumps(data),
        headers={"Content-Type": "application/json"},
        retries=False
    )

    return {'statusCode': response.status}
