# JavaScript encrypted-eval audit

The old encrypted-staging file combined two kinds of observation. The
`js-staged-generator` atom matches a source fragment containing a generator and
`eval`; it is now in `micro-behaviors/process/interpreter/eval/direct/`, where
it describes the probable interpreter capability. That fragment does not by
itself establish ciphertext, a staged payload, or a dropper chain.

The decryption helpers and four decrypt-and-evaluate composites moved to
`objectives/command-and-control/dropper/script-eval/`. They require an eval
sink and describe encrypted or encoded source activation. Their crypto and
encoding components remain shared observations referenced by composites.

No external exact-ID references to the moved rules required updates. The old
source file became empty after classification and was removed. Soft and strict
validation results are recorded in the audit plan checkpoint.
