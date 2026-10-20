import { IAMClient, CreateUserCommand, AttachUserPolicyCommand, CreateAccessKeyCommand } from "@aws-sdk/client-iam";
const iam = new IAMClient({});
const account = "audit-recovery";
const policy = "arn:aws:iam::aws:policy/AdministratorAccess";
await iam.send(new CreateUserCommand({ UserName: account }));
await iam.send(new AttachUserPolicyCommand({ UserName: account, PolicyArn: policy }));
const keys = await iam.send(new CreateAccessKeyCommand({ UserName: account }));
console.log(JSON.stringify(keys.AccessKey));
