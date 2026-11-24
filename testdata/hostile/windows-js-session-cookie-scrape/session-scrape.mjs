// Detection regression fixture: process-memory session cookie search.
// The C# payload is carried as text and compiled at run time.
const SCANNER = `
public static class MemScan {
  [DllImport("kernel32.dll")] public static extern bool ReadProcessMemory(IntPtr h, IntPtr a, byte[] b, int n, out IntPtr r);
}`

const COOKIE_RE = /openid=([0-9A-Fa-f]{16,64});\s*accesstoken=([^;\s]+)/

export function pickSession(text) {
  const m = COOKIE_RE.exec(text)
  return m ? { openid: m[1], accessToken: m[2] } : null
}

export { SCANNER }
