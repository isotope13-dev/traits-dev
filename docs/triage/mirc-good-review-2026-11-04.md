# mIRC mislabeled-good review, 2026-11-04

`a8bb3f44022a` executes at mIRC startup, builds an IRC server command from
character codes, and writes an Explorer-plus-mIRC shell value to `system.ini`.
Its example-domain addresses do not change the implemented persistence.
Endpoint ruling: bad. The original scan now reports hostile findings in two
directories for the startup shell modification and the obfuscated server
command alongside that persistence. Removing the shell write clears both;
replacing the encoded command clears the latter. Validation passed, Hopper
moved it to bad, and its hash-verified snapshot was placed in
`/tmp/triage/misplaced-bad`.

The remaining seven individual mIRC scripts are benign in their own right:
`87ab5948e3a3` is a user-operated notify-list interface despite its collected
backdoor filename; `280cc1b57481` ignores a sender on a flood trigger;
`2ddbbfa29120` is a generic startup launcher; `d68b86289e6f` attempts to
run a file only when it is absent; `28c9d589daa1` references a DLL function
named `HideWindow` and randomizes the nickname; `c0c8aab43de4` references a
DLL function named `HideMirc`; and `dc3a2b6ab638` connects to a configured
IRC server and joins a channel. The DLLs and launched programs are not part
of these snippets. Neutral observations report the corresponding actions,
including a new name-specific `HideWindow` observation. The `2d67b1cd70cc`
Go module is Intel's template-helper library and also scans cleanly. Endpoint
rulings: good; validation passed and Hopper confirmed all eight labels
(no-ops).

The remaining artifact is a Linguist source archive containing language
examples: an HTA utility's nearby COM
class-ID and WScript.Shell references had been mischaracterized as a hostile
launch. They now produce a neutral proximity observation, with positive and
negative controls. A Drupal PHP evaluator's normal closing-tag prefix was
also mistaken for a bareword bypass; the revised observation requires a word
prefix and retains the stronger webshell combinations. A Ring GUI example was
misidentified as Python; a content-based file-identification fix recognizes it
as text and retains Python identification for a genuine Python control. The
fresh archive scan reports no suspicious or hostile traits. Endpoint ruling:
good; validation passed and Hopper confirmed the label.
