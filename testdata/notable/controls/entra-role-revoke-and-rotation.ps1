Remove-MgRoleManagementDirectoryRoleAssignment -UnifiedRoleAssignmentId $env:ASSIGNMENT_ID
$roleDefinitionId = '62e90394-69f5-4237-9190-012177145e10'
Add-MgApplicationPassword -ApplicationId $env:APPLICATION_ID -PasswordCredential @{DisplayName = 'scheduled-rotation'}
