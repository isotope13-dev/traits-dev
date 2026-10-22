Static-table query regression controls
======================================

The original top-level alternative and the independent query patterns produce
the same `metadata/lang/source/shape::javascript-literal-tables-pure-helpers`
decisions on these nine files. Controls cover both property orders, multiple
subject keys, three separate arrays, strings interspersed with numbers, the
minimum table count, and import/impure-call suppression.

Expected matches: `both-record-orders.js`, `forward.js`, `reverse.js`, `sparse-arrays.js`, `three-arrays.js`.
