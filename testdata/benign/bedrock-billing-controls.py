import boto3
session = boto3.Session()
runtime = session.client("bedrock-runtime")
runtime.converse(modelId="amazon.nova-lite-v1:0", messages=[])
credits = session.client("billing").get_credits(accountId="123456789012", startDate=0)
