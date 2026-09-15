-- Decodes data to a file; does not invoke a shell on the decoded text.
set payload to "U0NQVF9EQVRBX09OTFk6IG9yZGluYXJ5IHJlcG9ydCBkYXRh"
do shell script "printf %s " & quoted form of payload & " | base64 -D > /tmp/report.txt"
