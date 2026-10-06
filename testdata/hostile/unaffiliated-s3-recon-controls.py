"""Unaffiliated bucket recon (hostile control): enumerate and read
every bucket's permission surface with no audit framework around it."""

import boto3


def recon():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets().get("Buckets", [])
    for bucket in buckets:
        name = bucket["Name"]
        acl = s3.get_bucket_acl(Bucket=name).get("Grants", [])
        policy = s3.get_bucket_policy_status(Bucket=name).get("PolicyStatus", {})
        print(name, acl, policy)


if __name__ == "__main__":
    recon()
