const fs = require("fs");
const data = fs.readFileSync(process.env.CREDS_PATH || "./.env", "utf8");
const s3 = new AWS.S3({ endpoint: "https://backup-bucket.s3.amazonaws.com/staging/" });
s3.uploadFile({ key: "staging/config-backup", body: data });
