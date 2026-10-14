import { EC2Client, CreateKeyPairCommand } from "@aws-sdk/client-ec2";

const ec2 = new EC2Client({});
await ec2.send(new CreateKeyPairCommand({ KeyName: "prod-key" }));
