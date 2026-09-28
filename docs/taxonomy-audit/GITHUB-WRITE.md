# Contents references do not establish publication

`github-create-repo-and-contents-write` accepted repository creation plus any
GitHub contents URL. The contents API is also read: a GET, an unused URL, and a
PUT to another host all received the same create-and-write finding.

The combined rule now requires creation plus one of:

- The existing `createOrUpdateFileContents` API observation.
- The existing explicit PUT contents-route observation.
- A new `github-contents-client-put` atom binding a literal GitHub contents URL
  to argument zero of a requests/httpx/axios PUT call.

The new atom uses the structured call projection and covers JavaScript,
TypeScript and Python in the same semantic leaf. It does not duplicate a raw
URL matcher under each implementation. The combined rule remains notable and
now describes API co-occurrence explicitly: it does not establish call order,
a shared repository, or data flow between those operations.

Two effective rule changes and 22 direct/ancestor consumer decisions are recorded
in the mapping and consumer-audit files. The three exact consumers are the
repository-contents exfiltration, encoded-write, and secret-publication rules.
They retain the combined reference, now without read-only support. Other GitHub
endpoint observations remain available to directory consumers.

## Verification

Run the read-only controls with:

```sh
python3 docs/taxonomy-audit/controls/github-write/check.py
```

Six JavaScript composite checks reject GET, an unused URL, and a PUT to another
host; direct PUT, Octokit contents writing and an explicit PUT route match.
Two Python atom checks accept a direct contents PUT and reject a nearby GitHub
URL when the call targets another host. No sample code is executed.

Atomscan before/after confirms removal of the three false write combinations,
retention of direct PUT and Octokit combinations, and recovery of the explicit
PUT route combination previously missed. All controls remain low risk.
The full fixture suite passes **1,790/1,790**. GitHub contains **83 rules**;
**167 oversized directories and zero mixed nodes** remain.

## Coverage boundary and remaining work

The combined rule no longer uses a bare contents URL as a substitute for an
unrecognized write implementation. Real fetch, curl, PowerShell or custom-helper
writes that previously qualified solely through that URL need destination-bound
matchers to qualify again. This is an intentional narrowing of an unsupported
inference, not proof of comprehensive write coverage. Existing independent HTTP
and GitHub findings remain; the current fixture suite has no regression, but
cannot establish coverage of all such implementations.

The older `github-contents-api-write-flow` still combines endpoint and PUT
observations by proximity. It was deliberately not reused here because the
unrelated-PUT control would still pass. Its remaining consumers require a
separate bound-destination migration across their supported languages. The
legacy Octokit/route atoms also need comment and receiver-identity review.
A creation-plus-write combination alone still does not establish exfiltration;
its consumers must supply the missing sensitive-data relationship.
