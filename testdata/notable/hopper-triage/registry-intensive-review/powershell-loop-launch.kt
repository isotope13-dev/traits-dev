object StatusMonitor {
 private val script = """while ($true) { Write-Output status; Start-Sleep -Milliseconds 700 }"""
 fun watch() { ProcessBuilder("powershell", "-NoProfile", "-NonInteractive", "-Command", script).start() }
}
