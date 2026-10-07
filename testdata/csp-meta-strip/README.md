Source: https://cert.gov.ua/article/6319983 (UAC-0277), linked by
https://securityaffairs.com/200537/hacking/cert-ua-fake-cloudflare-checks-deliver-lunexstealer-malware.html.

The advisory describes LUNARAXE.STRIP removing response CSP headers and CSP
meta tags and monitoring their reintroduction. These synthetic partial
components reproduce that behavior with WebRequest filtering and a DOM
MutationObserver. They do not identify LUNARAXE or reproduce its entire
stealer. Both findings are suspicious because policy modification also has
rare legitimate debugging uses. No campaign name or network indicator is
required by the traits. The samples use Chrome and WebExtension browser APIs.

cases.json records positive JavaScript/TypeScript cases and near misses:
non-CSP meta deletion, reading without deletion, a mismatched callback binding,
commented-out code, meta-only stripping, and a header filter that retains CSP.
The combined finding describes co-occurrence rather than proven execution or
data flow. The meta matcher binds the selected callback node to the removal
receiver; it intentionally covers the direct forEach arrow-expression form.
