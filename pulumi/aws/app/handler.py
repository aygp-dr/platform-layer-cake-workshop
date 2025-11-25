import os
import boto3

def handle(event, context):
    table_name = os.environ.get('TABLE_NAME')
    return {
        "statusCode": 200,
        "body": f"Connected to Layer 2: {table_name}"
    }
