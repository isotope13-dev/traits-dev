# Stored script fixture review

The three `stored-sandwich-script-injection` fixtures contain script-like
text in HTML attribute values. Parsing each document produces no script start
tag: the embedded `<script` text begins inside a quoted attribute. The
textarea example has a malformed attribute whose later quote changes parsing,
but it also produces no script start tag. The comments describe an intended
reflection scenario, which the artifacts do not themselves implement.

The fixtures therefore belong in the suspicious pool as inert injection-like
content. The former hostile composite inferred a remote script load from text
inside an attribute; it has been removed. Suspicious content observations
remain, and active exploit implementations remain eligible for hostile
findings through their own evidence.
