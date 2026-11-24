// SSRF protection for outbound personal-data-server requests.
export function safeProtocol(url) { return new URL(url).protocol === 'https:'; }
