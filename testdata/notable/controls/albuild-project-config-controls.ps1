function Read-ALbuildProjectConfigFile {
    <#
    .SYNOPSIS
        Reads one ALbuild project config file (albuild.json) from an app folder.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)] [string] $Folder
    )

    $file = Join-Path -Path $Folder -ChildPath 'albuild.json'
    if (-not (Test-Path -LiteralPath $file)) { return $null }
    return Get-Content -LiteralPath $file -Raw | ConvertFrom-Json
}

function Export-ALbuildProjectSummary {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)] [string] $Folder
    )

    $config = Read-ALbuildProjectConfigFile -Folder $Folder
    return $config
}
