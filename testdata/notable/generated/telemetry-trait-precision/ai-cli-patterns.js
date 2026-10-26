// Benign AI-CLI shapes that must NOT read as device telemetry, AWS
// billing, or downloader activity. The `?model=` query carries an LLM
// name, `getCredits` is a local credit-balance helper, `curl` sits in an
// intent-classifier alternation, and `require(TARGET)` is a test-template
// placeholder (still a bare uppercase require form, neutrally labeled).
import { getCredits } from "./api.js";

const TOOLWORDS = /\b(npm|npx|node|git|ssh|curl|grep|find|ls|cat|cd|mkdir)\b/;

export async function fetchExperience(cfg, model, topic) {
  const r = await fetch(
    cfg.baseUrl + "/experience?model=" + encodeURIComponent(model || "") + "&topic=" + encodeURIComponent(topic),
    { headers: { "X-Token": cfg.token } }
  );
  return r.ok ? r.json() : null;
}

export async function showBalance(cfg) {
  return (await getCredits(cfg)).credits;
}

export function loadTarget() {
  // Filled in by the test harness with a real path before running.
  const m = require(TARGET);
  return m;
}
