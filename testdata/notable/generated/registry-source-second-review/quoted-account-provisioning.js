// Cross-language representative of disposable-mail account provisioning.
const mailApi = "https://api.mail.tm";

export async function provisionIdentity(address, mailPassword, accountPassword) {
  await fetch(`${mailApi}/accounts`, {
    method: "POST",
    body: JSON.stringify({ address, password: mailPassword }),
  });
  const mailboxAuth = await fetch(`${mailApi}/token`, {
    method: "POST",
    body: JSON.stringify({ address, password: mailPassword }),
  }).then((response) => response.json());

  const protection = await fetch(
    "https://sentinel.openai.com/backend-api/sentinel/req",
    { method: "POST", body: JSON.stringify({ flow: "oauth_create_account" }) },
  ).then((response) => response.json());
  const protectedHeaders = { "openai-sentinel-token": protection.token };

  await fetch("https://auth.openai.com/api/accounts/authorize/continue", {
    method: "POST",
    headers: protectedHeaders,
    body: JSON.stringify({ username: { value: address, kind: "email" } }),
  });
  await fetch("https://auth.openai.com/api/accounts/user/register", {
    method: "POST",
    headers: protectedHeaders,
    body: JSON.stringify({ username: address, password: accountPassword }),
  });
  await fetch("https://auth.openai.com/api/accounts/email-otp/send", {
    headers: protectedHeaders,
  });

  const inboxHeaders = { Authorization: `Bearer ${mailboxAuth.token}` };
  const inbox = await fetch(`${mailApi}/messages`, { headers: inboxHeaders }).then(
    (response) => response.json(),
  );
  const message = await fetch(`${mailApi}/messages/${inbox["hydra:member"][0].id}`, {
    headers: inboxHeaders,
  }).then((response) => response.json());
  const otp = message.text.match(/\b\d{6}\b/)[0];

  await fetch("https://auth.openai.com/api/accounts/email-otp/validate", {
    method: "POST",
    headers: protectedHeaders,
    body: JSON.stringify({ code: otp }),
  });
  await fetch("https://auth.openai.com/api/accounts/create_account", {
    method: "POST",
    headers: { "openai-sentinel-so-token": protection.token },
    body: JSON.stringify({ name: "Generated User", birthdate: "1999-04-12" }),
  });

  const oauth = await fetch("https://auth.openai.com/oauth/token", {
    method: "POST",
    body: new URLSearchParams({ grant_type: "authorization_code", code: "captured-code" }),
  }).then((response) => response.json());
  return { "access_token": oauth.access_token, "refresh_token": oauth.refresh_token };
}
