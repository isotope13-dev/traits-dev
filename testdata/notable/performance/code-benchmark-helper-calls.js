// Static analysis fixture; never execute.
// Exercise every permitted helper form without treating calls as record data.
import { dedup } from './benchmark.js';

export const BENCHMARK_CASES = [
  { text: 'first', expectedRuleIds: ['RULE-001'] },
  { text: 'second', expectedRuleIds: [] },
  { text: 'third', expectedRuleIds: ['RULE-003'] }
];

const seen = new Set();
const unique = [];
for (const s of BENCHMARK_CASES) {
  const text = s.text.toLowerCase().trim();
  if (!seen.has(text)) {
    seen.add(text);
    unique.push(s);
  }
}
export const normalized = dedup(unique.filter(keep));
