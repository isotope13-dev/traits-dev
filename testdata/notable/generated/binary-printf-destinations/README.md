# Binary printf destinations

Small x86-64 ELF relocatable controls, compiled with
`clang --target=x86_64-linux-gnu -c control.c -o control.elf`.
Each source declares `const char command[]` containing the command below.
These are static matching controls; they do not execute the embedded commands.

| Fixture | Command | File-write atom | Null redirect |
| --- | --- | --- | --- |
| file | `printf '%s' data > /tmp/result` | yes | no |
| null | Cobra-style `printf -v comp "%%q" "${compline%%%%$tab*}" &>/dev/null` | no | yes |
| embedded-null | `printf` of a quoted shell script containing `>/dev/null 2>&1`, followed by backslash-newline and `> /tmp/helper` | yes | yes |
| null-prefix-file | `printf '%s' data > /dev/null-report` | yes | no |
| continuation | `printf '%s' data` followed by backslash-newline and `> /tmp/result` | yes | no |

The file-write atom is
`micro-behaviors/fs/write/file/redirect::binary-shell-printf-file-write`;
the null observation is
`micro-behaviors/process/fd/stdio::binary-devnull-output-redirect`.
Check atoms rather than presentation-filtered `any:` grouping composites.
The null control reproduces an actual embedded Grype/Cobra completion command.
Existing `registry-second-review` shell controls additionally retain real file
writes and exclude null-device and `/dev/tcp` destinations.
