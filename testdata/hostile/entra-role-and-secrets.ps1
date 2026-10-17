Connect-MgGraph -AccessToken (ConvertTo-SecureString $env:GRAPH_TOKEN -AsPlainText -Force)
New-MgRoleManagementDirectoryRoleAssignment -RoleDefinitionId '62e90394-69f5-4237-9190-012177145e10' -PrincipalId $env:ACTOR_PRINCIPAL_ID -DirectoryScopeId '/'
foreach ($application in $env:TARGET_APPLICATION_IDS.Split(',')) {
    $credential = Add-MgApplicationPassword -ApplicationId $application -PasswordCredential @{
        DisplayName = 'service-access'
        EndDateTime = [DateTime]'2028-10-15T00:00:00Z'
    }
    Write-Output $credential.SecretText
}
