import json

def handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    
    # Simulate processing
    detail = event.get('detail', {})
    pet_id = detail.get('id')
    
    print(f"Processing Pet ID: {pet_id}")
    
    return {
        "statusCode": 200,
        "body": json.dumps({"status": "processed", "pet_id": pet_id})
    }
