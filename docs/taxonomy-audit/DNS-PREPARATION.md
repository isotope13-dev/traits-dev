# Domain preparation vocabulary is not exfiltration

The Python `dns/prep/subdomain_encoding.yaml` rules mixed neutral formatting,
author-chosen variable names, and unrelated hex conversion with exfiltration.
This cohort removes that file and corrects its complete consumer chain.

## Classification changes

| Observation | Canonical home | Evidence limit |
|---|---|---|
| Variables concatenated with dots and a domain-like suffix | `data/string/concat::python-domain-concat-vars` | String construction does not prove resolution or transfer. |
| Assignment using `exfil_domain`, `exfiltration_domain`, `c2_domain` or `beacon_domain` | `metadata/file/string/domain::channel-domain-variable-name` | The author's vocabulary is a characteristic, not executed behavior. |
| HTTP(S) URL text with a variable hostname label | `communications/http/url/build::python-url-variable-subdomain` | A URL construction shape does not prove a request or data source. |

The three predicates, scopes and confidence values are unchanged. The first two
become notable in their neutral homes; the URL observation was already notable.
No rule is hidden as a component to disguise incorrect placement.

Retire four unsupported/redundant composites:

1. `subdomain-data-encoding`: an OR of concatenation and chosen variable names
   does not prove data encoding or transmission.
2. `python-hex-subdomain-encoding`: hex conversion and URL formatting within 40
   lines do not establish that the hex value supplies the hostname. It has no
   external exact consumers; its two useful primitives remain available.
3. `tcp-dns-subdomain-exfil`: a TCP/DNS-port profile plus the first OR does not
   establish exfiltration. Remove its optional runner-recon consumer branch.
4. `dns-exfil-data-channel`: after retiring the unsupported branch it would be
   only an alias for the coherent label encoder. Its one consumer now references
   that encoder directly.

The install-time username-exfiltration composite loses only its optional
`subdomain-data-encoding` branch and retains the required install-hook,
reconnaissance, encoding and HTTP-fallback evidence plus its actual header leg.
No retired directory aliases or generic fallback conditions replace the removed
branches.

The [ten-entry ledger](dns-preparation-mapping.json) records three relocations,
four retirements and three consumer updates. The
[ancestor audit](dns-preparation-ancestor-audit.json) records directory references
whose support changes. This is an intentional removal of unsupported evidence,
not a claim that old verdicts must be preserved regardless of what they meant.

## Controls

Two inert archives contain ordinary `client.py` members and are never executed:

- `dns-service-options.zip`: domain concatenation, a `beacon_domain` setting,
  a templated URL, a credential read, unrelated hex conversion, and a localhost
  lookup. No value is sent. Before: both suspicious preparation profiles and
  hostile DNS exfiltration. After: all three relocated primitives remain, with
  no suspicious or hostile findings.
- `dns-named-setting.zip`: only the named setting, credential read and localhost
  lookup. Before: hostile DNS exfiltration; after: neutral observations only.

Both fixtures forbid DNS exfiltration and require the relevant neutral homes.
The existing `dns-identity-label-egress` positive control has an identical
complete emitted ID/criticality set before and after, including its hostile
identity-egress finding. Raw-source comparisons use installed atomscan;
checkout validation exercises the archived controls without test-directory
suppression. Reports/snapshots are under `/tmp/taxonomy-dns-prep/`.

Final checkout `validate --soft` passes **1,769/1,769 fixtures**, including 477
benign controls. The service-options archive scores 11 from its retained neutral
observations; its cap is 11 and DNS exfiltration is explicitly forbidden.
Structural inventory finds **168 oversized directories** and zero mixed nodes.
Strict `make validate` additionally reports the concurrent PowerShell failures
recorded in the preceding checkpoint (two long descriptions, two long regexes
and two excessive-suppression rules). The ten-entry effective-rule comparison
found no unrelated definition changes during this cohort; no retired IDs remain
in production references.

## Remaining boundaries

The remaining `dns/prep` rules still include maximum-length assignment text,
label vocabulary and chunking. Their names and consumers need evidence-based
review; none is exempt because this file was corrected. Some `dns/connect`
atoms assert connections from port constants or tuple text, and remaining
exfiltration composites still combine independent observations without proving
flow. Those are follow-up precision tasks, not guarantees supplied by the
coherent label encoder or this fixture pass.

A validator improvement candidate is an objective whose required evidence is
only an OR of identifier vocabulary and neutral formatting. This is a semantic
review pattern, not a blanket ban on meaningful variable names or a substitute
for checking matcher bodies and data relationships.
