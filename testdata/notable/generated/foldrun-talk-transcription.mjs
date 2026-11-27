const settings = {};
const key = pick(flags.key, env.FOLDRUN_GATEWAY_KEY, env.ANTHROPIC_AUTH_TOKEN, env.ANTHROPIC_API_KEY, settings.ANTHROPIC_AUTH_TOKEN, settings.ANTHROPIC_API_KEY);
const base = flags.url || env.FOLDRUN_GATEWAY_URL;
await fetch(`${base}/v1/foldrun/transcribe?lang=${lang}`, {
  method: "POST",
  headers: { authorization: `Bearer ${key}`, "content-type": "audio/wav" },
  body: wav,
});
