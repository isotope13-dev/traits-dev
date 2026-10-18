2026-10-18: JSP command/file-control and ASP.NET SQL-console triage

Assessment is from source execution paths, not feed labels or scanner scores.
All three original files were scanned with atomscan and cleave facts. Facts
contained raw source, no decoded payloads, no parsed Java/C# flow, and no
external dependency records. The samples were not executed on a live server.

322807a2af30c73616c67862e736796f59efe1508ee0fe6ddb1e04f10ef72c06
菜刀jsp修改.jsp — MALICIOUS; Chopper-style JSP webshell.

EC(s,c) returns s unchanged: this version uses plaintext request values.
The parameter named by Pwd selects an A-Q dispatcher; Pwd is a parameter
name, not a password comparison. z1 and z2 are operator-controlled.
M builds argv from z1.substring(2), z1.substring(0,2), z2, invokes
Runtime.exec(c), and returns stdout/stderr through MM and the response.
For example, -c/bin/sh selects /bin/sh and -c with z2 as command text.
C/D read/write an unrestricted caller-chosen file. E recursively deletes;
F returns file bytes; G decodes uppercase hex pairs and writes them;
H/I/J copy, rename and create directories; K sets file modification time;
L retrieves an operator-selected HTTP URL into an operator-selected path.
N/O/P enumerate database catalogs, tables and columns. Q runs caller SQL,
returns rows, and falls back from executeQuery to executeUpdate.
Responses use split ->| / |<- delimiters. No fixed C2 URL, privilege
escalation, reverse connection or cryptographic decryption is established.

0d19a60d367de332a296a7070e86a0c537bad0ba2ff48af1768c6de84c086f71
sql.aspx — BENIGN; standalone ASP.NET SQL Server query console.

The Execute button calls btnExecute_Click. txtConnection.Text becomes
SqlConnection.ConnectionString; txtSql.Text becomes SqlCommand text.
ExecuteReader runs the supplied statement; a read loop builds an HTML table
and assigns it to Literal1.Text. Exceptions are printed; the connection is
disposed in finally. The inputs are unrestricted and this page provides no
authentication of its own. Its SQL capability is real and is retained as
notable API findings, but arbitrary database administration alone does not
prove a hostile objective. There is no built-in xp_cmdshell, OS execution,
credential theft, hidden payload, destructive SQL, or outbound data theft.
The external source may have collected it as a database webshell because an
intruder can use an exposed query console after gaining a server foothold.
That possible use does not establish malicious behavior in these bytes.

The two URL references are the W3C XHTML namespace and transitional DTD.
Fetched the namespace page, DTD and all three referenced character-entity
tables (xhtml-lat1.ent, xhtml-symbol.ent, xhtml-special.ent). They contain
standard markup definitions and numeric character entities, not executable
payloads. The namespace page contains no script element. These references
are markup identifiers, not server-side HTTP execution paths. System.Data
and System.Data.SqlClient are framework imports, not remote loaders.

Fetches and full initial/final scan reports are retained in the named scratch
workspace under scratch/jsp-triage, outside this trait repository.

ecf43efae44a4fb4078bc7da76e07cc10fe4e92fc145b58d7999f0cc2b902cde
SJavaWebManageV1.4.jsp — MALICIOUS; SJavaWebManage 1.4 webshell.

The page declares V1.4-20160528. PASS is MD5(test). Login sets a session
flag, but the non-Login branch only calls sendRedirect when the flag is
absent; it never returns before the command/file dispatchers. Redirecting
does not terminate servlet execution. Its advertised simple web-management
purpose therefore includes a remotely accessible OS/file control surface
with an ineffective authentication guard and a known default password.

CMDS reads cmd/encode through getRequestStringVal. That helper returns
request.getParameter(key). Util.execCmd splits cmd on spaces, puts the
parts after cmd /c or /bin/sh -c, executes Runtime.exec(cmds), reads output,
and returns it for rendering. On POSIX, splitting means only the first
command token is sh's command string; following tokens become positional
parameters. Single-token commands and shell metacharacters remain effective.
FileManage takes path and content from the same request getter and forwards
them to FileUtil.writeTextToFile, whose BufferedWriter writes text through
FileOutputStream(path). Other branches upload raw multipart data, read and
download files, recursively delete, create files/directories and ZIP selected
paths. There is no filesystem confinement or extension restriction.
DBManage uses caller JDBC driver/URL/credentials, runs caller SQL, browses
metadata, exports rows to a caller-selected local path or HTTP response.
EnvsInfo prints JVM properties. MD5 is password hashing, not encryption.
The version-check URL is emitted as a browser script src. Menu items for
port scanning, brute force, reverse control and remote control are only
javascript:void(0) links; those behaviors are not implemented here.

Detection changes

Two hostile composites cover both JSP implementations, across request/command
and file-manager. A suspicious request-to-argv atom and a notable
request-path/content-to-file atom require the actual forwarding code. Keys,
passwords, banners, filename and URLs never select them. Whitespace-tolerant
source signatures reflect the available facts: these JSP carriers have no
parsed Java data-flow projection. They conservatively recognize these two
implementation shapes rather than claiming arbitrary Java taint analysis.
Assignment guards reject input overwrites, and comment spans cannot supply
required source snippets. Hostile composite precision scores are 4.7 and 6.0.

Removed jsp-command-temp-file-source: its bare CMD substring matched a CSS
selector, not a temporary file. Existing consumers use the actual servlet
parameter observation instead. Narrowed the response-writer spelling so
System.out logging does not supply JSP response evidence. Stream-accessor
observations now say multiple input/output accessor calls, without guessing
whether the receivers are processes, sockets or HTTP connections.

Moved firing classloader/loading and reflective-instantiation facts out of
data/source into JVM runtime and metaprogramming/reflection respectively.
Moved DOM element creation into ui/window/dom/create, SQL execution into
data/db/query, and updated exact consumers. The compound class-loading
observation now describes API-reference co-occurrence, not proven loading.
The existing ADO.NET atoms now include ASP.NET's asp carrier; query-method
observations live under query instead of access. Pure umbrella composites
may be omitted by the renderer; tests assert the actual atomic observations.

Capacity review kept established leaf budgets at 100. Consolidated the two
implementation alternatives into one observation per operation. Relocated
String[] constructor lookup from webshell commands to neutral reflection,
Lua append-mode opening to append, and noncryptographic x65599 multiplication
to data/checksum. These relocations preserve matcher/scope/criticality;
exact consumers were updated. Removed a redundant Steam DOM leg already
covered by its UI directory selector. No global budgets or exclusions changed.

Run: python3 testdata/taxonomy/jsp-forwarded-request/check.py

20 controls cover both forwarding shapes with arbitrary parameter keys,
fixed and overwritten commands, overwritten argv, fixed file data, block and
line comments, neutral servlet behavior, ASP.NET SQL APIs and placement
observations. The focused checker disables third-party signatures so its
negative verdict assertions test local YAML. Unmodified third-party
SigBase/WEBSHELL/JSP/Writer/Nano separately matches the neutral fixed-command
control; sample rescans retain third-party scanning and receive no exclusion.

The dom-tree-operations benign archive expectation requires the relocated
DOM construction home and retains its prohibition on window-access claims.
