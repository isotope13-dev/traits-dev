// Benign near-miss: defensive threat-intel helper that quotes the campaign
// IOC strings without any browser-extension API context. The locker identity
// requires extension API usage in the same file, so this must stay non-hostile.
const CAMPAIGN_IOCS = [
  "cloudapi.stream",
  "cloudapi.stream/check_code_lock",
  "cloudapi.stream/auth_google",
  "cloudapi.stream/user_info",
];

async function reportSightings(sightings) {
  const reply = await fetch("https://intel.example.internal/api/sightings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ indicators: sightings }),
  });
  return reply.json();
}

function isCampaignHost(value) {
  return CAMPAIGN_IOCS.some((marker) => value.includes(marker));
}
