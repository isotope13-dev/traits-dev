First-party installer one-liners are not droppers
====================================================

The pipe-to-shell dropper traits fired on OpenClaw's own documented
install command (`iwr -useb https://openclaw.ai/install.ps1 | iex`) inside
a markdown code fence. The taxonomy already suppresses other vendors'
official installers this way (ollama, bun, unsloth, skillshare); OpenClaw
now has the same `official-install-ps1-url` context trait, referenced from
all three firing traits (`ps-iwr-pipeline-eval`,
`ps-command-wrapper-useb-remote-eval`, `ps-network-eval-pipeline`).

Run `python3 testdata/powershell-official-installer-url/check.py
<scratch-directory>`. `untrusted-pipe-positive.ps1` must report all three
traits; `install-doc-negative.md` must report none of them.
