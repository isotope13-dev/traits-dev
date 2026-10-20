# Abliterated-model payload regression fixtures

Inspired by [ProjectDiscovery's research](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned).
The `model-backdoor-*` files under `../hostile/` and `../benign/` are
synthetic static-analysis inputs. Never execute the shell fixtures. They
contain no credentials; URLs are placeholders and are never fetched by the
validation suite.

Coverage:

- `shell-curl-hidden-output`: downloading to a hidden file is suspicious by
  itself, including relative dotfiles and combined output flags such as
  `-sfo`. A visible output filename does not qualify.
- `shell-dotenv-loop-http-upload`: a loop-selected dotenv filename supplies
  the contents of a curl request body.
- `shell-private-key-loop-http-upload`: the loop-selected private key under
  `.ssh/` supplies that body. A `.pub` suffix does not qualify.
- `shell-hidden-temp-download-execute`: curl downloads a hidden temporary
  script and a following `&&` invokes the identical quoted or unquoted path.
- `serialized-agent-hidden-temp-shell-chain`: a single JSON `exec_command`
  request contains a hidden temporary download and shell invocation. JSON key
  order and escaping do not matter. This rule inspects top-level `name` and
  `arguments` fields, rather than arbitrary nested conversations, and does
  not assert that the two paths are identical.

These findings are suspicious: the observable command or transfer warrants
review, but these fixtures cannot establish authorization, execution, poisoned
weights, or a model's trigger. No rule depends on the article's trigger phrase,
collector hostname, model identity, or payload basename.

Positive variants cover renamed variables, braced expansions, different
collectors, curl argument order, guarded and unguarded loops, redirects, and
renamed temporary paths. Controls cover local-only reads, unrelated uploads,
variable reassignment, public keys, literal command text, discarded reads,
different execution paths, checksum verification between download and launch,
ordinary tool calls, split calls, and the trigger phrase alone.
Download-only, checksum, and different-launch-path controls retain the
suspicious hidden-download finding while excluding the execution chain.

Exact required/forbidden traits and score bounds are registered in
`../expectations.toml`; run `make validate CLEAVE=cleave` from the repository
root. The attack-shaped fixtures use the existing `hostile/` corpus with
suspicious finding floors, since the detections deliberately make narrower
claims than a hostile verdict.
