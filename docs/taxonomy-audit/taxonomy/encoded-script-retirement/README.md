# Encoded-script retirement

The 21 remaining rules in `command-and-control/dropper/staging/encoded/script`
have moved to their subjects, leaving the legacy leaf empty. Rules with likely
execution of reconstructed source moved to transformed-source evaluation;
response-to-file staging moved to acquisition; self-deletion and hidden WMI
launch moved to their respective behaviors. Generic COM, MZ, comparison and
loop co-occurrences became suspicious evidence profiles where they did not
establish a payload or launch. Names no longer attribute a family or network
behavior that the predicates do not require.

Two dependencies also imposed 200 KB limits. A 209,030-byte example containing
nearby `Resp` and `onse` string fragments showed that the ResponseBody fragment
cluster was skipped solely because of its size. The four bounds on that
cluster and the bound on a short-key/character observation have been removed.
The latter matches one key/value entry rather than a complete map and is now a
component. The self-deletion composite's download annotation was replaced with
its supported self-deletion technique.

[moves.json](moves.json) records original rules, effective defaults and the
migration decisions. Run
`uv run docs/taxonomy-audit/taxonomy/encoded-script-retirement/check-moves.py`
to verify them and
`python3 docs/taxonomy-audit/taxonomy/encoded-script-retirement/check-padding.py`
to check the formerly size-limited ResponseBody cluster.
