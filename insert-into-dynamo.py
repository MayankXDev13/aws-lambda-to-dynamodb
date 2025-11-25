import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print("EVENT:", event)

    try:
        # API Gateway sends JSON inside `body`
        if "body" in event and isinstance(event["body"], str):
            body = json.loads(event["body"])
        else:
            body = event

        # Validate input
        required_fields = ["lerarner_id", "lerarner_name", "lerarner_location"]
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        "error": f"Missing required field: {field}"
                    })
                }

        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.Table("learners")

        item = {
            "lerarner_id": body["lerarner_id"],
            "lerarner_name": body["lerarner_name"],
            "lerarner_location": body["lerarner_location"],
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Item inserted successfully",
                "data": item
            })
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "DynamoDB Error",
                "details": str(e)
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Unknown Error",
                "details": str(e)
            })
        }
