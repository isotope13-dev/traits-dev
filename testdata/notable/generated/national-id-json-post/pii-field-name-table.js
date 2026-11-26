// Near-miss regression fixture: a PII classifier keeps a table of field names
// and a regex alternation names the national identity field. Neither holds a
// national identity number, and the JSON POST carries a count only.
const PII_PATTERNS = ["ssn", "dob", "national_id", "tax_id", "phone", "email"];
const PII_RE = /\b(?:ssn|dob|national_id|tax_id)\b/i;

async function reportClassification(findings) {
  const counts = { pii: findings.filter((f) => PII_RE.test(f.field)).length };
  await fetch("https://telemetry.example.net/v1/counts", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(counts),
  });
  return PII_PATTERNS.length;
}

module.exports = { reportClassification };
