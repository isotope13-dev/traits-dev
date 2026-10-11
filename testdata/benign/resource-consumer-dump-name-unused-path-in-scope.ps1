# Public diagnostic stubs. Every function prints a fixed message; no filesystem, credential, encryption, or network operation is implemented here.
# These declarations are documentation examples for a command help page.
function dumpCredStore { Write-Output "public diagnostic" }
$reference = "application_default_credentials.json"
Write-Output $reference
