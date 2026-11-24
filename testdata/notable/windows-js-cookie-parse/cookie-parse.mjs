// Detection regression fixture: an OAuth client parses its own login cookie
// from a 302 response. It does not read any other process's memory.
const LOGIN_COOKIE = /openid=([0-9A-Fa-f]{16,64});\s*accesstoken=([^;\s]+)/

export function readOwnLogin(setCookieHeader) {
  const m = LOGIN_COOKIE.exec(setCookieHeader)
  return m ? { openid: m[1], accessToken: m[2] } : null
}
