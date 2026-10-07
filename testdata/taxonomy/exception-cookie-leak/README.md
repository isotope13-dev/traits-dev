The ordinary client sends the demonstrated base event but does not inspect
exception state. The error handler checks a server-side Ruby exception but
does not send the exploit trigger or extract credentials. Neither should fire
either exception-cookie-leak suspicious composite.

The threat-feed sample combines the article's screenshot-confirmed /ws base
event trigger, response read, missing-method error check and extraction of
session cookies from the serialized Cookie header. It intentionally uses a
generic session-cookie name rather than requiring Zammad's cookie name.

Source: https://horizon3.ai/attack-research/disclosures/cve-2026-102489-zammad-session-leak-rce/
The linked public GitHub PoC could not be retrieved. No package-install API
payload or privilege-escalation sample was invented. No malicious hash,
package release or remote endpoint was supplied by the article; localhost,
zammad.test and the screenshot's private IP are demonstration environment
values, and horizon3.ai is the publisher.
