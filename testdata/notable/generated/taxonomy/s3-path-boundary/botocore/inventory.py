import boto3
s3 = boto3.client('s3')
s3.list_buckets()
s3.get_bucket_acl(Bucket='example')
s3.get_bucket_policy(Bucket='example')
