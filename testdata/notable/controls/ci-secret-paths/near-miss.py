# Similar filenames and directories do not identify either credential store.
paths = [
    "/var/lib/jenkins/logs/initialAdminPassword",
    "/var/lib/jenkins/notsecrets/initialAdminPassword",
    "/var/lib/jenkins/secrets/initialAdminPassword.backup",
    "/etc/not-gitlab-runner/config.toml",
    "/etc/gitlab-runner/config.toml.example",
    "/etc/gitlab-runner/cache/config.toml",
]
