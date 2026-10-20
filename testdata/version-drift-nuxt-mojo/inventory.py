def inventory(s3):
    buckets = s3.list_buckets()
    return buckets, s3.get_bucket_acl(Bucket="media"), s3.get_bucket_policy(Bucket="media")
