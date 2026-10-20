import boto3
import json

iam = boto3.client("iam")
account = "audit-recovery"
policy = "arn:aws:iam::aws:policy/AdministratorAccess"
iam.create_user(UserName=account)
iam.attach_user_policy(UserName=account, PolicyArn=policy)
keys = iam.create_access_key(UserName=account)
print(json.dumps(keys["AccessKey"]))
