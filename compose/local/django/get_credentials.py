import boto3
import os
import json

s3 = boto3.resource('s3')
mapper = json.loads(s3.Object(os.getenv("DJANGO_AWS_STORAGE_BUCKET_NAME"), 'pm-credentials.json')
                      .get()['Body']
                      .read()
                      .decode("utf-8"))

with open('.source', 'w+') as infile:
    for k, v in mapper.items():
        infile.write(f'{k}="{v}"\n')
