// AWS SDK JS v3 client barrel shape (cf. @aws-sdk/client-s3 S3.ts): the
// service root re-exports *Command classes from ./commands/. The barrel
// implements bucket listing and permission reads as client operations;
// it is not permission reconnaissance.
import { S3Client } from "./S3Client";
import { ListBucketsCommand } from "./commands/ListBucketsCommand";
import { GetBucketAclCommand } from "./commands/GetBucketAclCommand";
import { GetBucketPolicyCommand } from "./commands/GetBucketPolicyCommand";
async function audit(client, bucket) {
  await client.send(new ListBucketsCommand({}));
  await client.send(new GetBucketAclCommand({ Bucket: bucket }));
  await client.send(new GetBucketPolicyCommand({ Bucket: bucket }));
}
export { S3Client, ListBucketsCommand, GetBucketAclCommand, GetBucketPolicyCommand, audit };
