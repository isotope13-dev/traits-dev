# Task dispatch and decryption outside the agent entrypoint: a module
# reusing the packet helpers is not the agent receive loop.
function Invoke-TaskHelper {
  Process-Tasking $Type $Data $TaskID
  $plain = Decrypt-Bytes -Key $Script:SessionKey -In $Tasking
}
