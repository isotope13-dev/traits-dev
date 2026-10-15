import { getGoogleCookies } from "./chrome-cookies.js";
import { isBrowserCookieAccessAllowed } from "./gemini-web-config.js";

export async function isGeminiWebAvailable(profile?: string) {
  if (!isBrowserCookieAccessAllowed()) return null;
  const result = await getGoogleCookies({ profile });
  if (!result) return null;
  return result.cookies;
}
