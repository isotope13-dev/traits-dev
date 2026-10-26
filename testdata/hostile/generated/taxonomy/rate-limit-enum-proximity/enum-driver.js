const CHECK_EMAIL_PATH = "/api/customer/account/check-email/";
async function sweep(payload) {
  const body = {emails: payload.list};
  for (const email of body.emails) {
    const r = await fetch(CHECK_EMAIL_PATH, {method: "POST", body: JSON.stringify({email})});
    if (r.status === 429) { await sleep(r.headers.get("retry-after") * 1000); continue; }
    results.push(await r.json());
  }
}
