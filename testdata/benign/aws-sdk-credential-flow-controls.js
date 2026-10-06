// Benign AWS SDK credential-flow controls: env credentials, SigV4 request
// signing, and API POSTs are the client's documented auth flow, not theft.
// Guards the acquittal of infrastructure SDKs (e.g. @stacksjs/cloud): none
// of the stealer/JSP/Lark/dropper readings below may fire here.
const AWS_ALGORITHM = "AWS4-HMAC-SHA256";

function loadCredentials() {
  return {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || "",
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "",
  };
}

async function callApi(payload) {
  const creds = loadCredentials();
  const res = await fetch("https://api.example.com/v1", {
    method: "POST",
    headers: { Authorization: signRequest(creds, AWS_ALGORITHM) },
    body: JSON.stringify(payload),
  });
  return res.json();
}

async function readSsmParam(ssm, name) {
  return ssm.getParameter({ Name: name });
}

function makeClient() {
  return new AWSClient({ region: "us-east-1" });
}

async function handleAuthPlain(challenge) {
  try {
    const pair = Buffer.from(challenge, "base64").toString("utf8");
    return pair;
  } catch (err) {
    throw new Error("504 Unrecognized authentication mechanism: " + err.message);
  }
}

module.exports = { loadCredentials, callApi, readSsmParam, makeClient, handleAuthPlain };
