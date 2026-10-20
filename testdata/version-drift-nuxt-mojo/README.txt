Nuxt DevTools 3.2.2 and django-mojo 1.37.1: BENIGN
================================================

Release comparison and identification
-------------------------------------
Fetched the immediately preceding stable releases from the primary registries:
https://registry.npmjs.org/@nuxt/devtools/-/devtools-3.2.1.tgz
https://files.pythonhosted.org/ (wheel URL in pypi.org/pypi/django-mojo/json).
Also fetched the target releases. Both target archives are byte-identical to
the supplied SHA256s. Nuxt tarballs match registry SHA512 integrity values;
Mojo wheels match PyPI SHA256 values. This verifies registry-byte agreement,
not publisher signatures or the security of arbitrary deployments.

Nuxt 3.2.1 SHA256:
4a0aa432a691b406bc8929faf9c51804e7f4dfa0e64b8fac7546f1cab2d6f05e
Nuxt 3.2.2 SHA256:
6793d05ed18ba5c3ecaac3bde58ea3f14ae87ac5f3e43f97da179d02fb171b07
Mojo 1.37.0 SHA256:
1455320f85a76dabcd22e60709f135d4b40476b08c558c86a531572b8cc147aa
Mojo 1.37.1 SHA256:
af2d54ee01ad8b9267cdadba696e9675eed17c24232dec1a09b1ff90a351b627

Nuxt DevTools
-------------
This is @nuxt/devtools, the development inspection UI and server integration.
The prior release was published 2026-02-12 and this one 2026-02-25.
The alleged payload is in the Quicktype type/schema-generation dependency.
The complete vendor bundles quicktype-core-f78dz8oi.js (old) and
quicktype-core-jebn1o7i.js (new) are BYTE-IDENTICAL, 1,245,430 bytes:
100c04b42cdf8fffea949d99ad6a888007dca6ddf083e8ef5275a3afb97ef6f6
The hashed asset filename changed; its content did not.

Decoded encodedMarkovChain: Base64 -> 148,193 gzip bytes -> 1,873,926 JSON
bytes, SHA256:
639ba5cb4cf454f81b0c0a6e0735bd57be8103f5fc024cffa6b7a85f4ddb63d4
Recursively checked the entire model: root keys trie/depth, depth 3,
3,101 count/arr nodes of width 128, 75,172 positive integer leaves and
318,656 null slots. Node counts are nonnegative (the root count is zero).
There are no string-valued commands, endpoints or executable fragments.

Execution path, traced through the minified modules:
DataSchemaDrawer -> jsonInputForTargetLanguage/InputData -> quicktype ->
inferMaps -> property-name scorer -> cached Markov load ->
JSON.parse(inflateBase64(encodedMarkovChain)). The decoder calls Base64.atob
and the bundled pako inflater with to:"string". evaluateFull indexes the
numeric character trie and computes geometric mean probabilities, used to
distinguish object properties from map keys. The decoded model is data;
it does not reach eval, Function, module loading or process execution.
The bundle's Function("return this") is a global-object compatibility shim,
independent of the model. The schema drawer displays/copies generated text.

Other release changes: 99 added and 79 removed member names, mostly rebuilt
frontend chunks; nine same-name members changed. The server adds scoped
storage watches and cleanup, Acorn changes from 8.15.0 to 8.16.0, and the
inspection component forwards attributes. Dependency updates include
launch-editor, simple-git and markdown-it; Quicktype remains pinned at 22.0.0.
The development-auth chunk verifies tokens with the local DevTools RPC and
synchronizes them through localStorage/BroadcastChannel. No install hook or
new payload activation is introduced. The model and its consumer explain
the alert better than compromise; no deployment-specific exposure is known.

Django Mojo
-----------
This is django-mojo, a Django REST framework with account, storage, deployment
and administrative AWS setup facilities. Prior wheel published 2026-10-19;
target wheel published 2026-10-20. The flagged aws_setup.py is BYTE-IDENTICAL
in 1.37.0 and 1.37.1, SHA256:
27bb66986ed75dd60b2c77617b822228c8875cc67786407c3e80a4c9ee3f19c7
The administrative frontend, mojo-bouncer.js and deploy/check_node.py are
also unchanged. Wheel METADATA changes only the version, not dependencies.

AWSSetupService gets clients through the configured boto3 credential chain.
discover_buckets checks the caller's account, bounds pagination, verifies one
canonical owner, and filters region, website hosting and installation tags.
It rejects public/cross-owner ACLs and unsafe bucket policies, then reads
public-access-block configuration. The admin's selected bucket is rechecked
before adoption; if necessary put_public_access_block enables all four
privacy controls and verifies them. The service tags the bucket, reconciles
CORS and registers a private default media FileManager. Web mutations require
system-admin authority through the setup orchestration; the CLI has an
explicit adoption path. This is convergent provisioning, not secret theft or
an attacker inventory channel. Credentials and cloud operations are real
capabilities, retained at notable severity; no actual installation context
or administrator authorization history is supplied.

The release adds a dry-run-by-default command to redact old SMS sign-in
secrets, redacts new SMS logs and limits stored relay metadata, strengthens
nested account-field/CSV/filter visibility and storage authorization, and
keeps older static chunks available across deployment generations. Reviewed
all 24 changed same-name members and the added management command. These are
access-control, privacy and deployment changes, not a new credential sink,
hidden execution path or arbitrary external destination. This positive
behavioral/diff evidence tips the verdict to BENIGN.

Trait corrections and migration
-------------------------------
Four S3 composites move from objectives/discovery/cloud/permissions to the
existing micro-behaviors/communications/http/services/aws-s3 leaf. Their
required evidence is listing, permission reads or a prefix-scoped lookup,
without an attack-specific action. moved-ids.json records every mapping.
The inventory composite becomes notable and explicitly describes same-file
co-occurrence; it does not prove listing-to-policy data flow. Removed its
ATT&CK attribution and the branding-based downgrade. Existing file-local
exclusions, type/platform constraints and default file scope are preserved.
The prefix rule's name no longer claims ownership from a name prefix alone.

Updated the cross-account consumer, the cloud-account-asset-enumeration
consumer and active fixture expectations. No other exact consumers or
permissions/cloud directory selectors select the moved rules. Three broader
objectives/discovery selectors (credential/reconnaissance and OOB callback
rules) intentionally lose these neutral observations; a capability should
not supply attacker-discovery evidence by tier membership alone. Existing
scope controls exercise SDK source, cross-member application behavior and
the certificate-plus-cloud consumer; all seven pass after the move.

The public-access-block update atom now requires a call, recognizes qualified
receivers and describes updating configuration rather than assuming it makes
the bucket private. A method reference does not fire. The setup.py path regex
now requires a path-component boundary; aws_setup.py no longer becomes
packaging-script context. Actual setup.py still matches.

Reclassified the old unbranded S3 inventory fixture as benign: the code only
lists buckets and reads policies; lack of a recognized scanner brand is not
hostile evidence. Ten focused controls cover inventory, listing-only,
read-only, method-reference near misses, configuration calls, basename
boundaries, prefix/unscoped lookups and the retained role-assumption consumer.
Run:
python3 testdata/version-drift-nuxt-mojo/check.py --work-dir <scratch-directory>

Scanner limitation and results
-----------------------------
Before the YAML corrections, rescans of both preceding releases reproduced
the original alerts; the claimed clean version baseline was not reproducible.
Final target scans have zero hostile traits. Mojo has zero suspicious traits.
Nuxt has one distinct suspicious trait, repeated at archive/carrier/layer:
binary/embedded/base64-gz. Cleave's embedded_code_detector.rs directly emits
it from Base64 plus gzip magic with suspicious severity and T1027.009.
Synthetic carrier findings are not YAML matchers and cannot be corrected
through a package exception. No ineffective YAML shadow or broad allowlist
was added. Encoding/container presence does not establish evasion; correcting
this remaining false suspicion requires an analyzer change outside this YAML
task. Both target verdicts are based on reverse engineering, not scan scores.

atomscan ran on both target paths before/after the changes and on both prior
releases, with --no-update --follow=none --mode slow. cleave facts ran on both
archives, the relevant source members and the decoded numeric JSON model.
Full reports, registry metadata, downloaded releases, inventories and source
diffs are retained in scratch/version-drift-review for this task.
Repository validation is run as the final task action: make validate.
