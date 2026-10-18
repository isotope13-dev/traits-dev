# Extensionless Node entry arguments

`node build/icons` does not prove a directory module or masquerading. Node
can resolve the entry to `build/icons.js`. UIkit 3.14.3 uses this command for
an SVG icon compiler; its scripts, dependencies and entire build tree are
unchanged from npm release 3.14.2. The manifest differs only in version.
The source diff changes DOM manipulation for older iOS and fixes the order
of parallax arguments; distribution changes concern UI behavior and builds.

Move the command-argument observation from
`objectives/evasion/masquerade/path::node-runs-asset-directory-as-module` to
`micro-behaviors/process/argument/file::node-entry-asset-basename` at notable.
The matcher still accepts both a build entry and `./public/fonts`, without
asserting resolution or intent. Separately, require `node` or `node.exe`
instead of accepting arbitrary four-character suffixes on the executable.

The sole exact consumer, the concealed folder-open task composite, now uses
the neutral argument trait and retains its independent activation and
concealment requirements. No ancestor directory selectors consume either
home. Other rules in the original leaf remain in place.

Controls cover the build command and a visible asset-name entry. Near misses
cover an explicit `.js` entry and another executable. The existing
`polinrider-dir-module-task.json.xz` control still detects concealed autorun;
only the unsupported suspicious argument finding becomes notable.
