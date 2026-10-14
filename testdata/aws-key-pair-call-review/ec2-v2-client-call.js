import AWS from "aws-sdk";

const ec2 = new AWS.EC2();
ec2.createKeyPair({ KeyName: "prod-key" }, (err, data) => {
  if (err) throw err;
});
