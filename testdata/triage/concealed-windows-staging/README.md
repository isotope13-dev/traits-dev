# Concealed Windows staging review

The non-Microsoft installer control removes Microsoft provenance claims from
an archive download/extract/launch script. It must not match either fake-update
hostile rule. Repeated curl fragments replace the tar fragment: repeating one
concealed tool must not satisfy the curl-and-tar conjunction.

Setup.vbs (fc2ec0fb4a24) reconstructs curl and tar, downloads an HTTP ZIP,
extracts it under Windows Temp, then selects an EXE folder member for Run or
ShellExecute with runas. Its Microsoft update header is deceptive. Option
Explicit plus undeclared xShGQGm/xShQa3h makes this specimen fail compilation;
static findings describe its written code, not successful runtime execution.

The 89e422e6a851 PE is a packed resource dropper, not established as Gh0st.
Isolated Unicorn emulation of the unpacker reached original entry 0x4045cc.
The restored code decrypts REGINST using alternating byte subtraction (27/62),
and IMAGE using three-position subtraction derived from its first two bytes.
REGINST is an executable helper. IMAGE is a DLL; its damaged MZ prefix is
restored by the loader. The code writes it, then starts rundll32 with RAFlush.
The outer executable falsely claims wininet.dll, including DLL version type.
The relocated signature requires that deceptive identity and the resource /
loader combination; it does not infer a family from packer section names.

The 970edea8be13 ZIP contains an obfuscated WSH JavaScript file disguised with
"pdf" in its member name. Its rotated string table resolves ScriptFullName,
Run, split, join, nodeTypedValue and SaveToFile. Star and punctuation removal
plus reversal recovers Base64 embedded stages; XMLDOM and ADODB.Stream stage
files before hidden Run execution. One recovered stage is a Lua virtualized
script supplied as an argument to the staged executable. Some identifiers are
unbound in this specimen; this does not make its concealed payload benign.

Delimiter removal is a neutral string-replacement operation. ActiveX
SaveToFile references plus string-table concealment are obfuscation, not an
ActiveX exploit. A nested call followed by '=' is syntax, not necessarily an
assignment (the VBScript specimen uses equality in an If condition).
