# Minimal Empire agent receive loop: entrypoint plus packet dispatch plus
# session-key decryption, without any code evaluation.
function Invoke-Empire {
  Process-Tasking $Type $Data $TaskID
  $plain = Decrypt-Bytes -Key $Script:SessionKey -In $Tasking
}
