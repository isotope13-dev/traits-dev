const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

function readOwnContainerEnvCount() {
  const selfPath = path.join('/proc', 'self', 'environ');
  const raw = fs.existsSync('/proc/self/environ') ? fs.readFileSync(selfPath, 'utf8') : '';
  return raw.split('\0').filter(Boolean).length;
}

async function checkOwnStsRole() {
  const ak = process.env.AWS_ACCESS_KEY_ID || '';
  const sk = process.env.AWS_SECRET_ACCESS_KEY || '';
  const host = 'sts.us-east-1.amazonaws.com';
  const body = 'Action=GetCallerIdentity&Version=2011-06-15';
  const amzDate = new Date().toISOString().replace(/[:-]|\.\d{3}/g, '');
  const day = amzDate.slice(0, 8);
  const hash = crypto.createHash('sha256').update(body).digest('hex');
  const sts = `AWS4-HMAC-SHA256\n${amzDate}\n${day}/us-east-1/sts/aws4_request\n${hash}`;
  const sig = crypto.createHmac('sha256', 'AWS4' + sk).update(sts).digest('hex');
  const res = await fetch(`https://${host}/?page=1&limit=10`, {
    method: 'POST',
    headers: { Authorization: sig, 'X-Amz-Date': amzDate },
    body,
  });
  return JSON.stringify({ envCount: readOwnContainerEnvCount(), ok: res.ok });
}

module.exports = { checkOwnStsRole };
