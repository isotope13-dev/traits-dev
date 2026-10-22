# Article 4078: concealed, self-removing install script

Source: https://www.aikido.dev/blog/software-supply-chain-security-best-practices

The saved teaser omits the article body. The live page cites malicious
`plain-crypto-js@4.2.1`, `axios@1.14.1`, `axios@0.30.4`, and
`postmark-mcp@1.0.16`. Its linked Axios report describes the platform-specific
dropper and cleanup. Forager recovered the original plain-crypto-js tarball
from the Huawei npm mirror. Its SHA-1 matches the report:
`07d889e2dadce6f3910dcbc253317d28ca61c766`. Its SHA-256 is
`58401c195fe0a6204b42f5f90995ece5fab74ce7c69c67a24c61a057325af668`.

The recovered `setup.js` assigns `__filename` to a const before unlinking it.
The new capability binds that declaration to the removal argument in the
adjacent statement, including comma expressions. It supports JavaScript and
TypeScript on Windows and Unix. Self-removal remains notable; a suspicious
composite additionally requires XOR reconstruction, Base64 decoding, file
writes, and a require inside try. These are co-occurring observations, not a
claim that the matcher proves decoded bytes reach the filesystem.

The canonical XOR reconstruction observation now covers TypeScript as well.
Family recognition requires actual XOR reconstruction and alternative campaign
markers, rather than requiring a chosen decoder name and key. The stq marker
requires an initial long string. The generic modular-index supply-chain trait
was removed: its matcher establishes arithmetic, and its required operation is
already represented by the decoder observations. It no longer counts toward
an install-hook conviction.

The original tarball has three hostile findings after the changes, plus the
new suspicious cleanup finding. The preceding fourth hostile install-hook
finding depended on the removed arithmetic leg. The artifact still exceeds
the hostile tier's two-trait floor.

Run the focused checks with the recovered script and Cleave's fixture path:

```sh
python3 testdata/taxonomy/article-4078/check.py \
  --artifact /path/to/recovered/package/setup.js \
  --fixtures-dir /path/to/cleave/tests/fixtures/threat-feed-4078
```

Seventeen cases cover the original, behavior-preserving re-encoded and renamed
JavaScript/TypeScript variants, benign cleanup, wrong paths, mutable aliases,
shadowing, comments, absent composite roles, and campaign markers without a
decoder. Generated controls stay in Cleave's fixtures. Temporary symlinks near
the recovered artifact remove the unrelated `/tests/fixtures/` path exception
from these focused behavior checks. No fixture is executed.

The variants change the key, arithmetic constants, campaign token, string-table
name, decoder names and cleanup alias. The script verifies that every decoded
command is unchanged. Neither variant fires the Axios family composite, while
both retain the new suspicious finding.
