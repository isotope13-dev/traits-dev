// Gemini Web fallback client. Uses the user's own session via the opt-in
// browserCookieAccess setting (default off); never exfiltrates cookies.
import { readBrowserCookies, buildCookieHeader } from "./reader.js";

const GEMINI_STREAM_URL =
  "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate";

export const BROWSER_COOKIE_ACCESS_SETTING = "browserCookieAccess";

export async function searchWeb(query, settings) {
  if (!settings || settings.browserCookieAccess !== true) {
    throw new Error("Gemini Web fallback requires browserCookieAccess=true.");
  }
  const found = await readBrowserCookies(["gemini.google.com"]);
  return { url: GEMINI_STREAM_URL, header: buildCookieHeader({}), query: found.query };
}
