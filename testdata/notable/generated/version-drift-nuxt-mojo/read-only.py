def permissions(s3):
    return s3.get_bucket_acl(Bucket="media"), s3.get_bucket_policy(Bucket="media")
