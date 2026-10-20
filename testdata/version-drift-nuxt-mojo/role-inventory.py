def inventory(sts, s3):
    sts.assume_role(RoleArn="arn:aws:iam::123456789012:role/audit", RoleSessionName="audit")
    s3.list_buckets()
    s3.get_bucket_acl(Bucket="media")
    s3.get_bucket_policy(Bucket="media")
