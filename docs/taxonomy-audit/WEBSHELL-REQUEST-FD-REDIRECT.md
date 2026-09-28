# ASP.NET socket relay taxonomy audit

The ASP.NET callback shell is a direct socket-to-process standard-stream
redirection technique. Its objective composite and two defining atoms now live
at their supported homes:

| Observation | Canonical home | Reason |
|---|---|---|
| `WSASocket` call reference | `micro-behaviors/communications/socket/create` | Probable socket creation is a neutral capability; the standalone clue is notable. |
| Child process stdin, stdout and stderr use the same socket | `objectives/command-and-control/reverse-shell/fd-redirect` | Direct descriptor attachment is the reverse-shell mechanism. |
| ASP.NET server-side script context plus both preceding observations | `objectives/command-and-control/reverse-shell/fd-redirect` | Required context and socket-to-process relationship form the objective. |

The combined rule still requires the ASP.NET script marker, `WSASocket`, and a
`CreateProcess` pattern assigning one socket to all three standard handles.
`stream-bridge` remains reserved for an explicit stream-copying or pumping loop.
The direct redirection does not require such a loop.

The old `webshell/request` leaf falls from **86 to 83** rules. The receiver
`reverse-shell/fd-redirect` rises from **35 to 37**, and neutral
`socket/create` rises from **61 to 62**. All are strict leaves below the
combined cap. The two atom matcher bodies are preserved; the process regex's
non-capturing group became an ordinary group with the same matched text. The
socket clue's severity changes from suspicious to notable because it is now a
neutral probable-capability observation. The hostile composite retains its
effective conditions and settings. No exact-ID consumers existed.

Three broader references were reviewed. `direct-http-c2` retains the combined
coverage through its existing webshell and reverse-shell alternatives. The
`php-full-webshell` conjunction loses the ASP.NET rules, whose declared types do
not match its PHP scope. CrystalX's command-and-control exclusion still covers
the moved rule under the same ancestor. No consumer matcher needed repair.

The controlled corpus passes **1,842/1,842 fixtures**, with no exclusions. It
includes a benign Telegram-path control: a session-data path is a useful path
observation, but does not prove reading, collection or export. The full live
validator remains non-green with **98 existing issues**, including **144
directories over the cap**. A separate concurrent addition has made
`micro-behaviors/data/serialize/schema-object` a 90-rule violator. The cap
migration remains open.
