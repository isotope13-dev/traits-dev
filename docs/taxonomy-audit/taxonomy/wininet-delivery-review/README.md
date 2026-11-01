# WinINet delivery review

The legacy API-based branch mixed process injection, staged acquisition,
file execution, C2 tasking and general API profiles. The AutoIt remote-thread
and RunPE combinations move with injection or hollowing; executable and
`agent.enc` download clues move to acquisition; process and ShellExecute
combinations move to their corresponding execution sinks. `agent.enc` is a
filename clue, not proof of an encrypted implant. An unsigned WinINet client
with virtualization names is a suspicious profile, not proof of VM evasion.
The `DOWNLOAD_RUN` token remains a component of C2 payload tasking.

The near-cap hollowing leaf was reviewed with its siblings. AutoIt source and
managed delegate rules move to the source and runtime hollowing branches. A
Go extended-startup observation and Explorer-parent combination move to
process-creation behaviors: those clues alone do not establish hollowing or
prove malicious parent spoofing. Exact references and the old dropper
ancestor's positive alternatives were updated.
