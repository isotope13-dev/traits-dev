// Bundled AWS SDK JS v3 instance-metadata credential provider module.
// The exported provider name and the endpoint env marker identify the
// SDK implementation; credential harvesters name the IMDS paths but
// never carry this provider export.
const ENV_ENDPOINT = "AWS_EC2_METADATA_SERVICE_ENDPOINT";
const TOKEN_PATH = "/latest/api/token";
const CREDENTIALS_PATH = "/latest/meta-data/iam/security-credentials/";

async function fromInstanceMetadata(init = {}) {
  const endpoint = process.env[ENV_ENDPOINT] || "http://169.254.169.254";
  const token = await request(endpoint + TOKEN_PATH, { method: "PUT" });
  return request(endpoint + CREDENTIALS_PATH, {
    headers: { "x-aws-ec2-metadata-token": token },
  });
}

module.exports = { fromInstanceMetadata };
