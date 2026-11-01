# Profile behavior review

Evidence with a supported behavior or objective should retain that meaning
even when the matcher does not prove a completed operation or data flow.

- Hidden-path chmod and nearby launch clues moved to local execution.
- Discord token-pattern and webhook clues moved to credential-token theft
  indicators; the description does not claim a completed transfer.
- A Swift `uploadTask` call moved to generic transfer. Its call name does not
  establish a URLSession receiver or HTTP transport.
- Shell heredoc and command-runner clues moved to source generation.
- Repeated multi-architecture FTP fetches and raw-IP wget/chmod/launch clues
  moved to payload execution. The ordinary curl/wget and PowerShell
  download-and-launch combinations moved to neutral deployment capabilities.

Existing exact consumers were updated. The local-execution and transfer
directory selectors were checked before the moves; the new upload finding
does not join the HTTP-specific upload directory. More rules remain in the
source profiles and need individual review.
