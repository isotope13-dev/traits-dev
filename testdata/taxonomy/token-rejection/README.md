# Token rejection and home destruction

Inspired by https://www.stepsecurity.io/blog/tensorlake-npm-compromised-hostage-token-worm .

Three static monitor fragments implement the described technique in shell,
Python and JavaScript. Each authenticates an HTTP request and places recursive
home-root deletion inside its HTTP 401/403 branch. No package name, service
name, campaign description, attacker endpoint or timer constant gates detection.
The hostile composites require a parsed HTTP-client call, Bearer-header evidence
and a parsed rejection/deletion conditional within 500 bytes. Header/request
co-occurrence does not prove the header belongs to that request; descriptions
therefore state co-occurrence. The branch itself must contain the deletion.

`cases.json` records three positives and nine controls. Controls change the
operand to a cache subtree, change the response condition to success, or replace
deletion with harmless error handling. All twelve expectations were checked
against `cleave --json testdata/taxonomy/token-rejection`; specimens were never
executed. The hostile precision scores were Python 5.7, JavaScript 6.5, shell 4.7
(before narrowing shell platform scope to unix).

The article evaluation samples are focused monitor fragments in the suspicious
tier: each yields one hostile and two suspicious traits. Full credential harvest,
package propagation and persistence are outside these fragments. Syntax coverage
is deliberately bounded to reviewed conditional/call forms, not every possible
spelling, indirection or obfuscator.

The shell home-delete atom also accepts a trailing slash on the bare home root
and requires a recursive flag; subdirectory deletion remains excluded. The Node
home-delete atom is described as a deletion call targeting home, since it does
not itself inspect the recursive option.

Full validation exposed missing generic YAML rule-type support in the installed
cleave engine. `cleave-yaml-support.patch` records the narrow FileType bridge,
YAML scope parser and structured-format selector fix against the local cleave
checkout; original YAML rules retain their original scope. Rebuilding local
engine sources with this bridge passes the existing YAML declaration controls
but reveals unrelated engine/corpus mismatches, so full validation is blocked.
The unrelated compatibility experiments have been removed. The older atomscan
embedded engine requires `CLEAVE_VALIDATE=0` and a compatibility copy where
six generic YAML scopes become GitHub Actions for scanning. The new threat
rules are identical in that copy. All article samples meet their detection
floors; the twelve focused fixture expectations passed on the installed engine.
