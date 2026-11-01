# Batch and Node response evaluation review

The nine batch and eight Node rules have been moved out of the legacy
response-eval taxonomy. Hidden PowerShell web launchers and network-fed Node
execution now live under their execution sinks. The Node decrypt/write/command
chain is classified by its likely file-execution behavior. Python's explicit
fetch/decode/exec source pattern is a neutral network-evaluation capability.

A SystemRoot-plus-expansions pattern describes syntax, not a PowerShell path.
Codepage remapping with that pattern is obfuscation evidence; it does not alone
prove a WebClient download or evaluation. The former WebClient composite no
longer accepts that unrelated alternative. The remaining alternatives require
hidden PowerShell, policy bypass and WebClient evaluation. Node HTTPS plus an
unbound eval reference, and HTTP POST plus a PHP URL and an RC4 call, are
suspicious evidence profiles rather than claims that a response was executed or
decrypted. The direct Node stream-to-VM pattern retains its execution claim.

The existing positive dropper ancestor selectors retain exact references to the
moved rules. Their evidence may still satisfy those broader historical
composites; revisiting those consumers' admission criteria is separate from
preserving this migration's directory membership.

The cryptography profile leaf contained 70 rules before this review. Nine
related key-recovery observations moved to the sibling key-recovery profile,
leaving 62 rules in cryptography after adding the HTTP/RC4 observation. No
cryptography-directory selector depended on the old location.
