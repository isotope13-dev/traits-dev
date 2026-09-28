import os
names = ["KUBECONFIG", "AWS_SECRET_ACCESS_KEY", "GOOGLE_APPLICATION_CREDENTIALS", "GITHUB_TOKEN"]
values = {name: os.environ[name] for name in names}
