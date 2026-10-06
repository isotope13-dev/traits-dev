Fixtures for objectives/impact/dos/parser/sql-expression.yaml.

The article's screenshot constructs 5,000 columns of 60 chained equality
operators. Detection is independent of parser identity and generating language.
The feed samples contain this SQL and a wider, whitespace-varied query embedded
in JavaScript. Both fire both suspicious traits. Stress tests can contain these
same structures, so the traits do not assert hostile intent or successful DoS.

Boundary expectations:

| Fixture | Expected parser trait |
| --- | --- |
| normal.sql | none |
| wide-shallow.sql | none |
| depth-below-threshold.sql | none (39 operators) |
| depth-at-threshold.sql | long-equality-expression-chain (40 operators) |
| width-below-threshold.sql | none (999 comma-terminated expressions) |
| width-at-threshold.sql | wide-deep-equality-projection (1,000 comma-terminated expressions) |

The width trait counts expressions with at least eight equality operators
immediately before a comma. A long chain alone does not imply a wide query;
a wide query of simple comparisons does not imply deep expressions.

Validated by cleave --traits-dir . --format json analyze testdata/parser-exhaustion,
with exact comparison of the parser trait IDs to the table above.
