def references(s3):
    return s3.list_buckets, s3.get_bucket_acl, s3.get_bucket_policy, s3.put_public_access_block
