function CredManMain {
    param([string]$DocumentationPath = './credentials-help.txt')
    # Display locally installed documentation for a credential-management UI.
    # This helper does not enumerate credentials or print stored passwords.
    Get-Content -Path $DocumentationPath
}
CredManMain
