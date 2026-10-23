async function gate() {
 const providers = ['https://ip-api.com/json/', 'https://ipinfo.io/json',
                    'https://ipapi.co/json/', 'https://geoplugin.net/json.gp'];
 const denied = ['IN', 'ID', 'ZA'];
 for (const country of ['IN', 'ID', 'ZA']) {
  if (new Date().getTimezoneOffset() === 180) return;
  const profile = await (await fetch(providers[0])).json();
  if (denied.includes(profile.countryCode)) return;
 }
 launch();
}
