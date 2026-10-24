# Renovate GitHub Action v44.2.4

Verdict: **BENIGN**. Sample SHA-256:
`67fc435288b9860ccf37edb0dba3ee3f0a4aaf90afa34489bd38462306878825`.
The artifact is the `renovatebot/github-action` source release, a Node 20
GitHub Action for running self-hosted Renovate in Docker.

## Decisive release comparison

Forager fetched the original preceding release:
`https://github.com/renovatebot/github-action/archive/refs/tags/v44.2.3.tar.gz`.
The archive and its `.forage.json` are retained in
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-28a4cdc2/scratch/version-drift-67fc/previous/generic/`.
All investigation outputs are under that scratch directory's parent.

Exactly four files differ between extracted releases:

* `.github/workflows/build.yml`: Renovate image version 42.71.0 becomes
  42.78.2, with the corresponding validator image digest update.
* `package.json`: release version, commitlint and typescript-eslint development
  versions, and pnpm 10.26.2 -> 10.27.0.
* `pnpm-lock.yaml`: corresponding development dependency resolutions, including
  transitive Actions libraries and undici. Runtime dependency pins stay fixed.
* `README.md`: action version references and example Renovate image version.

The flagged token step is unchanged. All runtime source files, `action.yml`,
`dist/index.js`, and its source map are byte-identical. The source map contains
114 source entries; its four application source bodies exactly match the
distributed `src/*.ts` files. Minification and source-map escape decoding are
ordinary build artifacts, with no newly introduced executable stage.

## Execution and verdict evidence

The e2e step checks whether RENOVATE_TOKEN is nonempty. One branch appends that
token to GITHUB_ENV; the other appends GITHUB_TOKEN under the same RENOVATE_TOKEN
key. Only one branch executes. Later `uses: ./` steps consume the selected token.
This provisions the expected authenticated Renovate test, rather than collecting
multiple credentials for an external recipient.

The action reads inputs and selected environment variables, resolves an optional
configuration file, validates token whitespace and file existence, and invokes
Docker through `@actions/exec`. It passes the configured token and environment to
the requested Renovate image, mounts configured paths, and optionally mounts the
Docker socket and obtains its group ID from `/etc/group`. It first invokes the
image with `--version`, then runs the configured container command. These
capabilities agree with its declared purpose. The bundled Actions/HTTP libraries
explain the network, crypto, file and process primitives. The reviewed execution
path contains no credential-export receiver, covert loader, or persistence.

Actual secret values, workflow audit history, and the contents of selected remote
Docker images are outside this artifact. No deployment or runtime success is
assumed. The unchanged implementation, explicit token plumbing and narrowly
bounded release diff tip the verdict benign. Scanner flow/embedded-source gaps
were addressed by manual inspection of the relevant source and workflow paths.

## Trait correction and consumers

The old suspicious objective
`objectives/credential-access/env/harvesting::shell-multiple-credential-variable-dump`
only counted two parsed credential-labeled file-write sites. It established
neither environmental acquisition, distinct runtime values, nor harvesting.
The real benign token fallback demonstrates the unsupported claim; a package
allowlist or GITHUB_ENV-wide exception would hide useful behavior.

The matcher and count are preserved under
`micro-behaviors/fs/write/credential::shell-multiple-credential-variable-writes`,
notable, with a description stating static write sites. Removed the unsupported
T1552.001 mapping. The underlying single-write trait is unchanged. Updated the
encoded-upload composite and the four ancestor credential-access selector
consumers (Feishu, Slack and two MCP rules) to preserve their previous member set.
Destination/ancestor filesystem selectors already admitted the underlying write;
the counted derivative adds no new matching population to those consumers.
No new directory or broader destination selector was introduced.

## Verification

`atomscan --no-update --follow=none --mode slow --format json <artifact>` was
run before and after on the sample, the preceding release and both original
LiteLLM workflow fixtures. `cleave facts` was run on the archive, workflow,
bundled JavaScript and original attack workflow. Reports are saved in scratch.

| Artifact/unit | Hostile before -> after | Suspicious before -> after |
| --- | --- | --- |
| v44.2.4 aggregate | 0 -> 0 | 1 -> 0 |
| build.yml archive member | 0 -> 0 | 1 -> 0 |
| e2e token run block | 0 -> 0 | 1 -> 0 |
| v44.2.3 aggregate | 0 -> 0 | 1 -> 0 |
| oct10-cache.yml aggregate | 0 -> 0 | 2 -> 1 |
| oct12-cache.yml aggregate | 0 -> 0 | 2 -> 1 |

The three sample occurrences are inheritance of one finding, not independent
behaviors. Every other sample detection is retained; aggregate notable count
changes 283 -> 284. The preceding release also fires before correction with the
current rules, contrary to the queue's earlier no-detection premise.

Classifier result is BENIGN before and after (class 0; live tiny output confirms
`scan benign confidence=0.810` after correction). Aggregate confidence changes
0.90813726 -> 0.80961674. The model warns that its v18 feature spec predates
expected v21, limiting interpretation of confidence changes. No remaining
rule/verdict disagreement was observed.

Both original LiteLLM attack workflows retain every other finding and the
suspicious encoded-file-upload technique at the same run blocks. Only the
generic write-count observation changes classification. Original attack
classifiers remain class 0 despite retained suspicious evidence, a pre-existing
classifier miss on these regression controls; no false objective was restored
to increase their scores. The focused checks verify renamed paths, aliases,
receivers, echo/printf, base64 variants, comments, quoted examples, missing
expansions, stdout/null sinks, single writes, decode-only and auth-only commands.

Commands (fixture scripts are analyzed, never executed):

```
python3 testdata/litellm-ci-staging-4228/check.py --evidence <scratch>/threat-feed/4228/testdata --fixtures <scratch>/version-drift-67fc/controls --report <scratch>/version-drift-67fc/controls-after.json
python3 testdata/version-drift-renovate/check.py --work-dir <scratch>/version-drift-67fc/placement-controls
```

Results: 16 staged-credential controls and 6 placement/consumer controls passed.
Final repository check: `make validate`.
