async function transcribe(env, flags, wav) {
  const pick = (...vals) => vals.find(Boolean);
  const base = pick(flags.url, env.GATEWAY_URL, env.ANTHROPIC_BASE_URL);
  const key = pick(flags.key, env.ANTHROPIC_AUTH_TOKEN, env.ANTHROPIC_API_KEY);
  return fetch(`${base}/v1/transcribe`, {
    method: "POST", headers: { authorization: `Bearer ${key}` }, body: wav
  });
}
