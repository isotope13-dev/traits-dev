// Legitimate hybrid app using Capacitor plugins and authenticated API POST.
export async function submitCheckin() {
  const { Geolocation } = window.Capacitor.Plugins;
  const pos = await Geolocation.getCurrentPosition();
  const token = localStorage.getItem('auth_token');
  const theme = localStorage.getItem('ui_theme');
  await fetch('https://api.company.org/v1/checkin', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ coords: pos.coords, theme })
  });
}
