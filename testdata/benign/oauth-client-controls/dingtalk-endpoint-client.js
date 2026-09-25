// Minimal DingTalk robot client: the DingTalk endpoint plus a credential
// field is what identifies this as DingTalk API usage.
async function sendDingTalkMessage({ dingToken, clientSecret, text }) {
  const res = await fetch('https://oapi.dingtalk.com/robot/send?access_token=' + dingToken, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ msgtype: 'text', text: { content: text }, clientSecret }),
  });
  return res.json();
}

module.exports = { sendDingTalkMessage };
