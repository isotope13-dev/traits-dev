import requests

# Network exploit markers without an HTTP operation.
proxy_path = "/public/..;/admin"
wordpress_url = "https://target.invalid/?pagename=one%252e%252e%252f%252e%252e%252fwp-content"
sqli_url = "https://target.invalid/item?id=1 OR 1=1"
artifactory_route = "/ui/stashResults/export"
artifactory_request = {"repoKey": "libs-release-local", "relativePath": "../../webapps/ROOT/../../etc/passwd"}
