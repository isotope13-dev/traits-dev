import {execFileSync} from 'node:child_process';

const command: string = String.raw`Connect-ExchangeOnline
New-InboxRule -Mailbox $env:MAILBOX -Name renamed -MarkAsRead $true -MoveToFolder "$($env:MAILBOX):\Conversation History"
New-InboxRule -Mailbox $env:MAILBOX -Name changed -MarkAsRead $true -MoveToFolder "$($env:MAILBOX):\RSS Subscriptions"`;
execFileSync('pwsh', ['-Command', command]);
