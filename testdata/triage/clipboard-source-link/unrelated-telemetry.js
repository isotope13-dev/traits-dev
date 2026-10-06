const report = 'app healthy';
setInterval(async () => {
  const clip = await navigator.clipboard.readText();
  if (clip) document.querySelector('#preview').textContent = clip;
  fetch('https://example.com/events?data=' + encodeURIComponent(report));
}, 2000);
