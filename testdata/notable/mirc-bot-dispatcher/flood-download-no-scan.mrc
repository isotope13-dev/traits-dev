[script]
alias parse {
  if ($1 == udp) { udp $2-  | halt }
  if ($1 == download) { http $2 }
  halt
}
