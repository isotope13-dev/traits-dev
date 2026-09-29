# CFML form declaration controls

Synthetic controls are parsed only, never executed. They cover seven control tag
kinds, literal/encoded/interpolated names, comments, raw text, quoted markup,
conditional attributes, wrong fields, unrelated tags and malformed declarations.
Server-side CFML operations in HTML contexts must remain detectable.

`datasource-original.cfm` is the unchanged reviewed datasource/command shell:
SHA-256 987de3c74aaa5371c98365b281fdc3c4b680558aae5b4c9895ec6b8c9fc083d2.
The runner also uses the independently decoded original retained in
`../cfml-directory-actions/retained-original.cfm`, SHA-256
110db2340e0aecb5c59d73b15617b28999d941f974ae04acf4d53ddcf945e9dc.
Both hashes are asserted. Both are malicious source fixtures; do not execute them.
