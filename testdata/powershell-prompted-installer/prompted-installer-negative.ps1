# Test fixture: interactive installer with retry and a one-shot bootstrap.
# The unbounded loop prompts the operator (Read-Host), the sleep is retry
# backoff, and the fetched script executes once. This must NOT report the
# poll-eval agent-loop hostile.
$MaxAttempts = 3
function Invoke-WithRetry {
    param([scriptblock]$Action)
    for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
        try {
            return & $Action
        } catch {
            if ($attempt -ge $MaxAttempts) { throw }
            Start-Sleep -Seconds (2 * $attempt)
        }
    }
}
function Read-YesNo {
    param([string]$Prompt)
    while ($true) {
        $response = Read-Host "$Prompt [y/N]"
        if ($response -match '^\s*[Yy]') { return $true }
        if ($response -match '^\s*$') { return $false }
    }
}
if (Read-YesNo 'Install helper') {
    Invoke-WithRetry { Invoke-RestMethod https://example.com/install.ps1 | Invoke-Expression }
}
