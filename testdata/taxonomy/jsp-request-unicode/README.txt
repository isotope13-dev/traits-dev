2026-10-18: JSP_KIT and Unicode CaiDao JSP webshell triage

Verdicts derive from complete source execution paths, not external labels,
trait names or model probabilities. Original samples were scanned with atomscan
and cleave facts; hashes match the requested SHA-256 values. JSP facts expose
no parsed Java calls or flow graph. The CaiDao text facts include two
UnicodeEscapeDecode runs containing the declarations and request scriptlet.
A separate one-pass Unicode decode was inspected in full. No sample was run
on a servlet container or used to launch a command.

MALICIOUS e0539a2d4e132884adc135c8438f7647ddd6be61f1f9d83966b12f17382a1296
1.jsp -- JSP_KIT Windows command webshell.

MALICIOUS a577587bd71c3928ba7902f147a18ab647e1478e0559ec1f213fcbf6c227b991
cmd_win32.jsp -- same JSP_KIT page, without the final newline.

The HTML POST form supplies cmd. On any request with that parameter, the page
calls Runtime.getRuntime().exec("cmd.exe /c " + request.getParameter("cmd")).
The supplied text is parsed as a Windows shell command under the servlet's
identity. It obtains the child stdout stream, reads lines through
DataInputStream, and prints each line to the HTTP response. The acquired
OutputStream is unused. There is no authentication, command allowlist, path
restriction, external payload, fixed callback URL, or dependency fetch.
Its declared command-execution purpose accurately describes an unrestricted
HTTP-to-shell backdoor. The two names are collector labels, not evidence.

MALICIOUS cf08b15de7c2039464782d7b370a7bf88e0565c0f643a9eb4b994a9ff2fea59b
CaiDao-Webshell-Password-LandGrey.jsp -- Unicode-escaped CaiDao-style webshell.

The Java compiler translates the Unicode escapes before tokenizing the Java
scriptlets. They reconstruct runnable declarations and request handling, not
an encrypted runtime payload. EC(s,c) converts Latin-1 bytes to the requested
charset; this is character encoding, not cryptography. Pwd="LandGrey" is the
name of a request parameter that carries an operation letter. No password
comparison or authentication takes place. z0 chooses the charset, and z1/z2
carry arguments. The resulting operation is dispatched as follows:

A: return the page's directory; enumerate drive roots on a Windows-style path.
B: list the caller's directory with sizes, timestamps and read/write flags.
C: read a caller-selected text file into the response buffer.
D: truncate/create a caller-selected file and write caller-supplied text.
E: recursively delete the selected path via EE and File.delete.
F: stream the selected file to the HTTP response between X@Y delimiters.
G: decode uppercase hexadecimal pairs and write the selected binary file.
H: recursively copy a selected file/directory to the selected destination.
I: rename a selected path. J: create a directory.
K: parse the supplied time and call File.setLastModified on the selected path.
L: open the supplied HTTP URL and copy its response to the supplied local file.
M: form argv = {z1.substring(2), z1.substring(0,2), z2}, call Runtime.exec(c),
   read stdout and stderr through MM, and return them to the operator.
   For example, -c/bin/sh becomes /bin/sh, -c, <z2 command>; /ccmd.exe
   becomes cmd.exe, /c, <z2 command>. The code itself embeds neither choice.
N/O/P: connect through the supplied JDBC driver and connection URL, select an
   optional catalog, enumerate catalogs/tables/column definitions.
Q: execute caller SQL, return rows, and fall back to executeUpdate on failure.

GC calls Class.forName on the supplied installed driver class and constructs
it, then uses DriverManager.getConnection. No bundled JDBC implementation or
remote code dependency is present. Network destinations are supplied at runtime;
there is no referenced fixed URL to fetch. The general response buffer is
framed by X@Y; errors are returned as ERROR:// text. FF resets the response and
closes its output stream, so subsequent generic output can fail on that path.
Sequential stdout/stderr reads can block on large output, without removing the
command-execution capability. All filesystem operations use the servlet's
existing permissions. No reverse connection, privilege escalation, credential
stealing routine, or cryptographic decryption is established.

Detection changes

The initial scans reported no suspicious/hostile traits for these files.
Added a direct cmd /c request-concatenation observation to the existing direct
and cmd-named JSP command composites. The matcher requires the shell prefix
at the actual execution expression; unrelated parameter reads plus a fixed
command, or a fixed executable with caller arguments, do not qualify.

Added conventional charset-helper/request-operand bindings and the contiguous
split-argv/exec statement. Text matching sees both plaintext and the decoded
Unicode layers, whereas existing inline YARA signatures see raw bytes and
expect an identity EC helper. A command composite requires both operand
sources, the complete charset helper, the argv sink and JSP syntax. A second
hostile composite requires the matching z1-path/z2-content writer. Neutral
capabilities stay in process creation, HTTP request access, codec and file
writing; Unicode escape presence stays in language encoding metadata.
Assignment and comment guards deliberately decline ambiguous lexical cases.
These signatures recognize common implementation forms; they do not claim
general Java taint analysis. Passwords, banners, framing, filenames and URLs
are not required. Exact sink snippets retain conventional local identifiers;
other implementations require their own supported forwarding evidence.
The existing SELECT-all SQL matcher now accepts lowercase SQL while preserving
the Java API's case-sensitive spelling. Removed the unsupported E1203
(client-exploitation) mapping from a decoded Runtime.exec reference.

Capacity/placement audit

No budgets were increased and no implementation-language directories added.
Removed jsp-shell and jsp-page-runtime-request-shell: both were redundant
subsets of jsp-cmd-parameter-runtime-exec, with no live exact YAML consumers.
Their stronger canonical finding remains. Removed the f-variable-only
FileOutputStream constructor subtype: the general constructor covers it and
the sole consumer's remaining FileOutputStream word matcher already subsumes
it at identical Java/OS scope. This preserves that consumer's match population.
Moved @event timer.action from process execution to a precisely named source
annotation observation. Preserved matcher, type and OS scope, changed the
unsupported suspicious level to notable, and updated its exact consumer.
An annotation alone does not launch a process. Ancestor exec selectors use
creation as evidence; the annotation does not belong in their member sets.
Relevant explicit exec/handle parent selectors were reviewed: none relies on
a count of the removed aliases. New split-argv and writer observations do
establish the creation/write operations selected by those parents.

Verification

Run: python3 testdata/taxonomy/jsp-request-unicode/check.py
29 controls cover direct and prefixed commands, arbitrary keys, Unicode code,
fixed commands and operands, overwritten inputs/argv/writers, alternate
converters, comments, SQL case and neutral annotation/constructor placement.
Run: python3 testdata/taxonomy/jsp-forwarded-request/check.py
20 existing JSP/ASP.NET/placement controls verify prior forwarding coverage.
Hostile composite precision for the charset command/file-write findings:
6.0 / 6.8; the direct/named-cmd composites score 4.4 / 6.3.
Precision is corroborative; source behavior and controls decide.
Initial/final scan JSON, complete facts and diagnostic output are in the
named scratch directory outside the trait checkout. Each original sample
receives exactly one .MALICIOUS marker. Final repository validation is run
after the scans, controls, report and markers are complete.
