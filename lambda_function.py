import json
import boto3
import os
import random
import time  # for calculating expiration time

# Initialize S3 client
s3 = boto3.client('s3')
URL_EXPIRATION_SECONDS = 300

def lambda_handler(event, context):
    file_name = event.get('queryStringParameters', {}).get('file_name', 'No fileName provided')
    content_type = event.get('queryStringParameters', {}).get('content_type', 'ContentType not specified')
    
    return get_upload_url(file_name, content_type)

def get_upload_url(key, content_type):
    
    # Calculate expiration time
    expiration = int(time.time()) + URL_EXPIRATION_SECONDS

    # Generate presigned URL from S3
    try:
        s3_params = {
            'Bucket': os.environ['UploadBucket'],
            'Key': key,
            'Expires': expiration,
            'ContentType': content_type
        }
        upload_url = s3.generate_presigned_url('put_object', Params=s3_params)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'uploadURL': upload_url,
                'Key': key
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
