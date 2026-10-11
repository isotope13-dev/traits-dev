Regression controls for unguarded-js-tail-recursion.
Copy fixtures to a scratch directory before cleave test-rules: the rule
intentionally excludes paths under testdata through its testing suppressors.
Expected matches: single.js, unguarded.js.
Expected nonmatches: guarded.js, interleaved.js.
All four expectations were verified using cleave test-rules and an independent
JavaScript tree-sitter query run. Both Highcharts versions also have zero
matches in ChartUtilities.js and accessibility.src.js.
