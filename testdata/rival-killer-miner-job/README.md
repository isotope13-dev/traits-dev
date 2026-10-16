Supervised background jobs are not rival-killing
==============================================

`killing-competing-malware` matched `kill -TERM "$miner"` in a
mutation-testing harness where `miner` is the script's own background job
(`miner=$!` for cargo-mutants, killed on timeout). `$!` is always the
script's own child; rival killers name someone else's process (killall,
pkill -f). The `unless` is file-scoped on purpose: `not:` only filters the
matched span, but the assignment and the kill live on different lines.

Run `python3 testdata/rival-killer-miner-job/check.py <scratch-directory>`.
`negative-job-control.sh` (supervise-and-timeout idiom) must not report
`killing-competing-malware`; `positive-rival-killer.sh` (pkill/killall by
name) must still report it.
