const BLOCKED_PATTERNS = [/captcha/, /checking your browser/];
export const blocked = BLOCKED_PATTERNS.some(pattern => pattern.test(html));
