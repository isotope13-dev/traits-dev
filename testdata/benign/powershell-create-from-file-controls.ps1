<#
.SYNOPSIS
Coverage helper control: builds scriptblocks from local source files to map
command lines, without executing them. Mirrors ansible-test's coverage_stub.ps1
idiom -- Create() fed straight from file content read off disk, no decoding
layer -- which must not read as a dynamic-execution loader.
#>
[CmdletBinding()]
param (
    [Parameter(Mandatory, ValueFromRemainingArguments)]
    [String[]]
    $Path
)

$stubInfo = @(
    foreach ($sourcePath in $Path) {
        [Collections.Generic.HashSet[int]]$lines = @()

        if (Test-Path -LiteralPath $sourcePath) {
            $code = [ScriptBlock]::Create([IO.File]::ReadAllText($sourcePath))

            $predicate = {
                $args[0] -is [System.Management.Automation.Language.CommandBaseAst]
            }
            $cmds = $code.Ast.FindAll($predicate, $true)

            $lines = @(foreach ($cmd in $cmds) {
                    $cmd.Extent.StartLineNumber
                })
        }

        [PSCustomObject]@{
            Path  = $sourcePath
            Lines = $lines
        }
    }
)

ConvertTo-Json -InputObject $stubInfo -Depth 2 -Compress
