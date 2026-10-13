import boto3
client = boto3.client("s3")
for x in range(500_000):
    print(x)
