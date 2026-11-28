// A server SDK reads its own parsed cookie header, without browser access.
export function identify(cookieHeader, apiKey) {
  const cookies = readCookieStore(cookieHeader);
  return cookies.get(getAnalyticsCookieName(apiKey))?.value;
}
