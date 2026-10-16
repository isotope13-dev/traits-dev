SAWFLY's documented technique evaluates decrypted POST code and returns 404
when its trigger is missing. The PHP reconstruction implements the reported
Base32/RC4 request and response transport; the OpenSSL variant changes the
cipher and encoding. Neither fixture is a recovered malware specimen.

Source: https://cloud.google.com/blog/topics/threat-intelligence/armory-castle-exploits-beyondtrust

Run `python3 testdata/encrypted-request-webshell/check.py` for static controls.
The controls check renamed helpers, changed request parameters, absent error
suppression, ordinary cipher code, a decryption endpoint without execution,
unrelated local evaluation, and inert quoted examples. A decoded request
without crypto or a 404 must not satisfy either new composite.

The cipher rule states co-occurrence with request evaluation, rather than
claiming proven cipher-to-eval data flow. The 404 rule likewise reports
co-occurrence with request-linked execution. Neither requires campaign
filenames, keys, parameter values, product identity or an RC4 function name.

Directory names and test markers cannot suppress the live request-to-eval
sink. Other existing evidence-based exceptions remain in effect. The fixtures
are analyzed as code and must never be served or executed.

The hexadecimal key exposed an existing classification error: a 64-character
hex literal alone does not establish SHA-256. That unchanged matcher now
records an encoding property; the SHA-256 comparison composite references it
alongside its existing hash-operation evidence.
