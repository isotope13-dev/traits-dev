# RTF, XLM and RAR document delivery review

The RTF byte-nibble, obfuscated object and malformed auto-update rules now
belong to document obfuscation. MathType object combinations and auto-updating
linked-object controls are RTF object profiles: the latter do not by themselves
prove exploitation of CVE-2017-0199. The XLM rules describe workbook
obfuscation and dispatch rather than an independently established payload.

The RAR stream-and-script rule matches archive-wide stream and script evidence;
it checks neither traversal nor that the script is in the stream. It and the
tiny document-themed HTML member rule now describe archive profiles. The RTF
rules' directory-name test suppressions were removed because the file path does
not make the document content benign. Generic obfuscation and object profiles
are suspicious rather than automatically hostile.

The associated InQuest-named rule was a byte-nibble pattern combined with a
common image name or greeting, which does not identify a malware family. Its
markers and composite are retained as an RTF profile without family attribution.
