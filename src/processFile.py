import os
import json

import boto3
import urllib3

TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
textract_client = boto3.client('textract')
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME, Key={"file_id": {"S": key}}
    ).get("Item")

    try:
        response = textract_client.detect_document_text(
            Document={'S3Object': {'Bucket': bucket, 'Name': key}}
        )
    except Exception as e:
        http = urllib3.PoolManager()
        callback_url = result.get('callback_url', {}).get('S', '').strip()
        response = http.request(
            'POST',
            callback_url,
            body=json.dumps({"file_id": key, 'error': 'Error with detecting text in document'}),
            headers={"Content-Type": "application/json"},
            retries=False
        )
        return {'error': str(e), "statusCode": 400}

    text_blocks = [block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE']
    text_blocks_set = set(text_blocks)

    if len(text_blocks_set) == 0:
        http = urllib3.PoolManager()
        callback_url = result.get('callback_url', {}).get('S', '').strip()
        response = http.request(
            'POST',
            callback_url,
            body=json.dumps({"file_id": key, 'error': 'Error with detecting text in document'}),
            headers={"Content-Type": "application/json"},
            retries=False
        )
        return {'error':'Error with detecting text in document', "statusCode": 404}

    item = {
        'file_id': {'S': key},
        'callback_url': {'S': result.get('callback_url', {}).get('S', '')},
        'text': {'SS': list(text_blocks_set)}
    }

    dynamodb_client.put_item(TableName=TABLE_NAME, Item=item)

    return {'statusCode': 200}
