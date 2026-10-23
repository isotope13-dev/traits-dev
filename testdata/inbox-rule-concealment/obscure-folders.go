package main

import "os/exec"

func main() {
    command := `Connect-ExchangeOnline
New-InboxRule -Mailbox $env:MAILBOX -Name renamed -MarkAsRead $true -MoveToFolder "${env:MAILBOX}:\Conversation History"
New-InboxRule -Mailbox $env:MAILBOX -Name changed -MarkAsRead $true -MoveToFolder "${env:MAILBOX}:\RSS Subscriptions"`
    if err := exec.Command("pwsh", "-Command", command).Run(); err != nil { panic(err) }
}
