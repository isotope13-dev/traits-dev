Hosts-file pharming redirect needs same-line proximity
========================================================

`security-domain-attacker-ip-redirect` pairs a public-IP hosts entry with
a security-domain target. The IP and the name share one hosts line, so the
composite requires both legs within 256 bytes. Without proximity, a large
text corpus assembles a redirect that was never written — X.509 OID
dotted quads far from an unrelated 360.cn address in a database dump.

Run `python3 testdata/hosts-pharm-proximity/verify.py
<scratch-directory>`. The same-line fixture must report the hostile; the
far-apart fixture must not.
