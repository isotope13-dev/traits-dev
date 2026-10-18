export const KNOWN_C2_DOMAINS: string[] = ["scan.aquasecurtiy.org", "staging.trycloudflare.com"];
export const KNOWN_BAD_NPM_VERSIONS: Record<string, unknown> = {};
export function checkIOCBlocklist(content: string) {
  return KNOWN_C2_DOMAINS.filter(domain => content.includes(domain));
}
