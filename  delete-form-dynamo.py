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

        # Validate required key
        if "lerarner_id" not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    "error": "Missing required key: lerarner_id"
                })
            }

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('learners')

        key_to_delete = {
            "lerarner_id": body["lerarner_id"]
        }

        # Perform delete
        response = table.delete_item(Key=key_to_delete)

        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "Item deleted successfully",
                "deleted_key": key_to_delete
            })
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                "error": "DynamoDB Error",
                "details": str(e)
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                "error": "Unknown Error",
                "details": str(e)
            })
        }
