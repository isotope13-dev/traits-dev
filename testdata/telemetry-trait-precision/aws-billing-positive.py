import boto3


def remaining_credits(account_id):
    session = boto3.Session()
    billing = session.client("billing")
    return billing.get_credits(accountId=account_id)
