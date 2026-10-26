$source = "Write-Output hello"
$task = [ScriptBlock]::Create($source)
Start-Job -ScriptBlock $task
