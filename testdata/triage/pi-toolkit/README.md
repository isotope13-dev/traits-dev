Pi toolkit 0.11.5 regression controls

The supplied npm archive SHA-256 is
77710e719dd0bd6e9ed4763bdd8f076195789955257586aa8b53e216a1df2190.
The package and four listed JavaScript members are BENIGN.

The installation hook copies bundled agent guidance, sets a default theme and
copies/chmods the worktree CLI and its shell completion. Browser automation
uses CDP; profile copying requires --profile, and the watcher stores browser
console/network metadata locally. The browser test uses isolated fixture HTML.
Subagent tests mock command dispatch and manage temporary files. Benchmark
preparation installs pinned runtimes and names local authentication seed files;
it has no credential upload. The native ppmd executable's main function selects
compression/decompression and uses pudutech PPMd file streams. Binwalk was not
available; the tar member inventory and rizin analysis supplied format/code review.

Changes require actual calls rather than method definitions, keep sensitive-path
matching inside the first read argument, retain restricted mode observations in
tests, recognize rsync in JavaScript template commands, and relocate generic npm
invocation and source identifier/option syntax to their supported homes. Literal
.exe process launches belong with argument-vector execution. stdout co-occurrence
requires a call and does not claim captured output.

The renamed execFile atom preserves its matcher and exact consumers. Broad
process/create/exec selectors now omit mere identifier text: actual execution
atoms remain in that subtree. npm invocation no longer enters publish selectors;
the explicit npm publish composite references the relocated atom. The --exclude
matcher preserves the exclusion composite's exact membership without claiming
that rsync is an archive utility. No software-name allowlist was introduced.

Controls:
- calls.js: exec call, sensitive literal read, restricted create and .exe launch.
- definitions.js: method definition, unrelated env statement and .exe in argv.
- npm-args.js: npm invocation without evidence for publication.
- rsync.js: template command and exclusion option, without archive attribution.
