function Invoke-SSHCommand
{
    param([String]$ComputerName, [String]$Command)
    # Depends on an SSHClient implementation with password auth support.
    $auth = New-Object PasswordAuthenticationMethod('admin', 'secret')
    $client = New-Object SSHClient($ComputerName, 'admin', $auth)
    $client.Connect()
    $res = $client.RunCommand($Command)
    $client.Disconnect()
}
