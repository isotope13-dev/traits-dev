import boto3
client = boto3.client("s3")
url = client.generate_presigned_url("get_object", Params={"Bucket": "owned", "Key": "asset"})
