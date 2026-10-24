// Only two array-valued expectation records count. Similar text, other keys,
// and an expectedRuleIds property with a non-array value must not count.
export const BENCHMARK_CASES = [
  { code: 'example', expectedRuleIds: ['RULE-001'] },
  { code: 'example', expectedRuleIds: [] },
  { code: 'example', expectedRuleIds: 'RULE-003' },
  { code: 'expectedRuleIds: []', otherRuleIds: ['RULE-004'] }
];
