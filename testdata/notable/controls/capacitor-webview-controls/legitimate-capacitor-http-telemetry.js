// Near-miss: a Capacitor page reads Device/Geolocation data and POSTs JSON to
// a cleartext HTTP endpoint on a public host with no collector-side marker
// (no cookie harvest, private-LAN address, OOB host, or proxy delivery).
// The sensing plugins themselves are legitimate app capabilities.
export async function syncFieldStatus() {
  const { Geolocation, Device } = window.Capacitor.Plugins;
  const payload = {
    device: await Device.getInfo(),
    position: await Geolocation.getCurrentPosition()
  };
  await fetch('http://status.partner-lab.org/field/v1', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
}
