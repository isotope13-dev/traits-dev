$mailbox = $env:MAILBOX
Connect-ExchangeOnline
New-InboxRule -Mailbox $mailbox -Name 'renamed-a' -From 'accountant@example.invalid' -MarkAsRead $true -MoveToFolder "${mailbox}:\Conversation History"
New-InboxRule -Mailbox $mailbox -Name 'renamed-b' -MarkAsRead $true -MoveToFolder "${mailbox}:\RSS Subscriptions"
