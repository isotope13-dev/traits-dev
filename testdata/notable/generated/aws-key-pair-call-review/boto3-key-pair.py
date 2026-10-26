import boto3

client = boto3.client("ec2")
client.create_key_pair(KeyName="prod-key")
