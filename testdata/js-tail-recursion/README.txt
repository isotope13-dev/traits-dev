Regression controls for unguarded-js-tail-recursion.
Copy fixtures to a scratch directory before cleave test-rules: the rule
intentionally excludes paths under testdata through its testing suppressors.
Expected matches: single.js, unguarded.js, mixed.js.
Expected nonmatches: guarded.js, interleaved.js, guarded-range.js,
guarded-children.js.
The original four expectations were verified using cleave test-rules and an independent
JavaScript tree-sitter query run. Both Highcharts versions also have zero
matches in ChartUtilities.js and accessibility.src.js.

The range and child controls reproduce guarded traversals in @cesium/engine
1.1.0 and 2.0.0. Both original source files are identical between those
releases. A missing first-child anchor let the query skip guards when a
declaration or loop separated them from the tail expression suffix.
mixed.js checks that this correction remains local to the matched function.
All seven controls passed an atomscan run after copying them out of testdata;
the popup-recursion composite still matches unguarded.js and mixed.js.
The singleton query arm preserves single.js on the engine's tree-sitter
implementation, which misses zero repetitions between the two anchors.
