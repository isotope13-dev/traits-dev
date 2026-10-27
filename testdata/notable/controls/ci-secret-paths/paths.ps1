$JenkinsPassword = 'D:\CI\Jenkins\secrets\initialAdminPassword'
$RunnerConfiguration = 'D:\GitLab-Runner\config.toml'
Write-Output @($JenkinsPassword, $RunnerConfiguration)
