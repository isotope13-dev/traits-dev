# JavaScript sensitive-data source split

This pass moved JavaScript export signals out of the generic
`objectives/exfiltration/sensitive-data` leaf according to the information the
matcher requires. The source leaf falls from **134 to 125 rules**. The wallet
leaf rises from **48 to 54**, and the generic credential leaf rises from **37
to 40**. These are combined atomic/composite counts; no cap exception was
introduced. `sensitive-data` remains above the 85-rule cap and still needs
source-by-source review.

The six wallet moves are the Fetch header atoms for seed and mnemonic values,
the factory-plus-header and seed-validation-plus-header classifiers, and the
wallet-password capture/export classifier. Each requires wallet-specific
evidence, so `stealer/wallet` is the single defensible source category even
though the HTTP header is the transport. The four composite classifiers retain
their matcher legs and effective platform, file-type, and archive scope. The
canonical seed-header classifier now carries both T1041 and T1552.001.

The three generic credential moves are the private-key input/request-field
helper, the user-entered private-key HTTP export classifier, and the
private-key environment-value HTTP export classifier. Their evidence does not
require a wallet source. The last rule was renamed from
`js-wallet-key-http-exfiltration` to `js-private-key-env-http-exfiltration`;
its environment-variable matcher is generic private-key material, not a
wallet-only key. Consumer references were updated, and the HTTP aggregate was
renamed from `js-wallet-key-material-transport` to
`js-credential-secret-transport` because it now combines generic private keys
with wallet-password export.

The supply-chain rule `library-wallet-seed-header-theft` had the same required
factory and seed-header evidence as the wallet classifier, with no package,
publication, or install-hook evidence. Its “library” label therefore added no
taxonomic fact. The duplicate was removed, and its ATT&CK mapping was unioned
into the canonical classifier. The DTS suppression was already guaranteed by
the wallet-factory evidence. There are no references to the retired rule ID.

All **1,842 controlled corpus fixtures** pass after overlaying the changed
taxonomy files on the last passing controlled snapshot. This confirms the
current expected corpus still scores; it does not mean the full taxonomy
validator is clean. Live `make validate` still reports broad pre-existing
catalog issues, including 144 over-cap directories. The moved definitions
produce no broken-reference or YAML-load errors in that run.

The duplicate suggests a validator improvement: compare composites after
expanding predicates already guaranteed by required legs. The current duplicate
composite check compares explicit conditions, so an extra `unless` clause can
hide a semantically redundant wrapper when a required leg already excludes the
same context. Such a check should report the overlap for review rather than
auto-merge rules whose taxonomy claims or ATT&CK metadata differ.
