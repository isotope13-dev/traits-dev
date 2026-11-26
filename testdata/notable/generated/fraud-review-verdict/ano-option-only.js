// Consent form helper (regression near miss, synthetic).
const consentRules = [
  {
    targetText: "ano",
    targetValue: "Y",
    selector: 'select[name="consent-marketing"]'
  }
];

for (const rule of consentRules) {
  for (const select of document.querySelectorAll(rule.selector)) {
    select.value = rule.targetValue;
  }
}
