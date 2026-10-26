// Site-analysis overlay: endpoint tooling hints for analysts.
const TOOLING_TIPS = {
  toolingGroup: "Endpoints grouped by required tooling (WAF bypass, authentication, signing, etc.)",
  severity: "Critical obstacle blocks data access without specific tooling",
};

// Technology fingerprint table: match page resource hosts to known
// providers so the report can label what serves each asset. Names below
// are identification labels, never capability claims.
// filler 00: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_00 = /\\.[a-z0-9-]+\\.cdn-provider-00\\.net$/i;
// filler 01: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_01 = /\\.[a-z0-9-]+\\.cdn-provider-01\\.net$/i;
// filler 02: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_02 = /\\.[a-z0-9-]+\\.cdn-provider-02\\.net$/i;
// filler 03: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_03 = /\\.[a-z0-9-]+\\.cdn-provider-03\\.net$/i;
// filler 04: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_04 = /\\.[a-z0-9-]+\\.cdn-provider-04\\.net$/i;
// filler 05: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_05 = /\\.[a-z0-9-]+\\.cdn-provider-05\\.net$/i;
// filler 06: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_06 = /\\.[a-z0-9-]+\\.cdn-provider-06\\.net$/i;
// filler 07: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_07 = /\\.[a-z0-9-]+\\.cdn-provider-07\\.net$/i;
// filler 08: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_08 = /\\.[a-z0-9-]+\\.cdn-provider-08\\.net$/i;
// filler 09: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_09 = /\\.[a-z0-9-]+\\.cdn-provider-09\\.net$/i;
// filler 10: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_10 = /\\.[a-z0-9-]+\\.cdn-provider-10\\.net$/i;
// filler 11: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_11 = /\\.[a-z0-9-]+\\.cdn-provider-11\\.net$/i;
// filler 12: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_12 = /\\.[a-z0-9-]+\\.cdn-provider-12\\.net$/i;
// filler 13: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_13 = /\\.[a-z0-9-]+\\.cdn-provider-13\\.net$/i;
// filler 14: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_14 = /\\.[a-z0-9-]+\\.cdn-provider-14\\.net$/i;
// filler 15: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_15 = /\\.[a-z0-9-]+\\.cdn-provider-15\\.net$/i;
// filler 16: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_16 = /\\.[a-z0-9-]+\\.cdn-provider-16\\.net$/i;
// filler 17: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_17 = /\\.[a-z0-9-]+\\.cdn-provider-17\\.net$/i;
// filler 18: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_18 = /\\.[a-z0-9-]+\\.cdn-provider-18\\.net$/i;
// filler 19: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_19 = /\\.[a-z0-9-]+\\.cdn-provider-19\\.net$/i;
// filler 20: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_20 = /\\.[a-z0-9-]+\\.cdn-provider-20\\.net$/i;
// filler 21: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_21 = /\\.[a-z0-9-]+\\.cdn-provider-21\\.net$/i;
// filler 22: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_22 = /\\.[a-z0-9-]+\\.cdn-provider-22\\.net$/i;
// filler 23: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_23 = /\\.[a-z0-9-]+\\.cdn-provider-23\\.net$/i;
// filler 24: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_24 = /\\.[a-z0-9-]+\\.cdn-provider-24\\.net$/i;
// filler 25: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_25 = /\\.[a-z0-9-]+\\.cdn-provider-25\\.net$/i;
// filler 26: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_26 = /\\.[a-z0-9-]+\\.cdn-provider-26\\.net$/i;
// filler 27: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_27 = /\\.[a-z0-9-]+\\.cdn-provider-27\\.net$/i;
// filler 28: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_28 = /\\.[a-z0-9-]+\\.cdn-provider-28\\.net$/i;
// filler 29: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_29 = /\\.[a-z0-9-]+\\.cdn-provider-29\\.net$/i;
// filler 30: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_30 = /\\.[a-z0-9-]+\\.cdn-provider-30\\.net$/i;
// filler 31: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_31 = /\\.[a-z0-9-]+\\.cdn-provider-31\\.net$/i;
// filler 32: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_32 = /\\.[a-z0-9-]+\\.cdn-provider-32\\.net$/i;
// filler 33: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_33 = /\\.[a-z0-9-]+\\.cdn-provider-33\\.net$/i;
// filler 34: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_34 = /\\.[a-z0-9-]+\\.cdn-provider-34\\.net$/i;
// filler 35: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_35 = /\\.[a-z0-9-]+\\.cdn-provider-35\\.net$/i;
// filler 36: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_36 = /\\.[a-z0-9-]+\\.cdn-provider-36\\.net$/i;
// filler 37: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_37 = /\\.[a-z0-9-]+\\.cdn-provider-37\\.net$/i;
// filler 38: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_38 = /\\.[a-z0-9-]+\\.cdn-provider-38\\.net$/i;
// filler 39: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_39 = /\\.[a-z0-9-]+\\.cdn-provider-39\\.net$/i;
// filler 40: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_40 = /\\.[a-z0-9-]+\\.cdn-provider-40\\.net$/i;
// filler 41: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_41 = /\\.[a-z0-9-]+\\.cdn-provider-41\\.net$/i;
// filler 42: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_42 = /\\.[a-z0-9-]+\\.cdn-provider-42\\.net$/i;
// filler 43: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_43 = /\\.[a-z0-9-]+\\.cdn-provider-43\\.net$/i;
// filler 44: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_44 = /\\.[a-z0-9-]+\\.cdn-provider-44\\.net$/i;
// filler 45: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_45 = /\\.[a-z0-9-]+\\.cdn-provider-45\\.net$/i;
// filler 46: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_46 = /\\.[a-z0-9-]+\\.cdn-provider-46\\.net$/i;
// filler 47: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_47 = /\\.[a-z0-9-]+\\.cdn-provider-47\\.net$/i;
// filler 48: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_48 = /\\.[a-z0-9-]+\\.cdn-provider-48\\.net$/i;
// filler 49: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_49 = /\\.[a-z0-9-]+\\.cdn-provider-49\\.net$/i;
// filler 50: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_50 = /\\.[a-z0-9-]+\\.cdn-provider-50\\.net$/i;
// filler 51: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_51 = /\\.[a-z0-9-]+\\.cdn-provider-51\\.net$/i;
// filler 52: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_52 = /\\.[a-z0-9-]+\\.cdn-provider-52\\.net$/i;
// filler 53: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_53 = /\\.[a-z0-9-]+\\.cdn-provider-53\\.net$/i;
// filler 54: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_54 = /\\.[a-z0-9-]+\\.cdn-provider-54\\.net$/i;
// filler 55: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_55 = /\\.[a-z0-9-]+\\.cdn-provider-55\\.net$/i;
// filler 56: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_56 = /\\.[a-z0-9-]+\\.cdn-provider-56\\.net$/i;
// filler 57: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_57 = /\\.[a-z0-9-]+\\.cdn-provider-57\\.net$/i;
// filler 58: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_58 = /\\.[a-z0-9-]+\\.cdn-provider-58\\.net$/i;
// filler 59: cdn hostname pattern entry placeholder for asset labeling
const CDN_PATTERN_59 = /\\.[a-z0-9-]+\\.cdn-provider-59\\.net$/i;
const TECH_RULES = [
  { id: "akamai", name: "Akamai", category: "cdn" },
  { id: "datadome", name: "DataDome", category: "protection" },
  { id: "perimeterx", name: "PerimeterX", category: "protection" },
  { id: "hcaptcha", name: "hCaptcha", category: "captcha" },
  { id: "recaptcha", name: "reCAPTCHA", category: "captcha" },
  { id: "turnstile", name: "Cloudflare Turnstile", category: "captcha" },
];
function detectProtection(scriptSrcs) {
  const found = [];
  for (const src of scriptSrcs) {
    const s = src.toLowerCase();
    if (s.includes("akamai")) found.push("Akamai");
    if (s.includes("datadome")) found.push("DataDome");
    if (s.includes("perimeterx")) found.push("PerimeterX");
    if (s.includes("hcaptcha.com")) found.push("hCaptcha");
    if (s.includes("recaptcha")) found.push("reCAPTCHA");
    if (s.includes("challenges.cloudflare.com")) found.push("Cloudflare Turnstile");
  }
  return [...new Set(found)];
}
