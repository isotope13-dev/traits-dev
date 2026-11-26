// Lender review dropdown setup (regression fixture, synthetic).
const reviewSelectRules = [
  {
    targetText: "ano",
    targetValue: "Y",
    keyHints: ["isnotliar", "overovaci otazky"],
    selector: 'select[name="select-isNotLiar"], [data-testid="isNotLiar-select"] select'
  }
];

for (const rule of reviewSelectRules) {
  for (const select of document.querySelectorAll(rule.selector)) {
    select.value = rule.targetValue;
  }
}
