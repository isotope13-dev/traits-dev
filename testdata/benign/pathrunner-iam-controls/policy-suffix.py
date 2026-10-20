import boto3
iam = boto3.client("iam")
policy = "arn:aws:iam::aws:policy/AdministratorAccess" + "-ReadOnly"
iam.attach_user_policy(UserName="analyst", PolicyArn=policy)
