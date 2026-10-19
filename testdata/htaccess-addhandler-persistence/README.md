PHP Apache handler and webshell boundary
=======================================

`htaccess-command-webshell-handler` requires a request-driven process console,
an htaccess write, and data-suffix PHP handler configuration within 2048 bytes.
AddHandler/AddType and FilesMatch/SetHandler are supported. Configuration alone
is notable; it does not establish a backdoor or persistence. The matcher reports
co-occurrence, without claiming the directive was the value written to htaccess.

Run `python3 testdata/htaccess-addhandler-persistence/verify.py <scratch-directory>`.
The controls also cover renamed request keys and data suffixes, unrelated output
handles, request data confined to descriptors, cyclic XOR reconstruction, a
WordPress init hook, and cookie-webshell setuid grants. Nothing is executed.
