import boto3
iam = boto3.client("iam")
iam.attach_role_policy(RoleName="audit", PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess")
