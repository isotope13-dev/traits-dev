function Write-SampleMessage {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string] $Message
    )

    Write-Information -MessageData $Message -InformationAction Continue
}

Export-ModuleMember -Function Write-SampleMessage
