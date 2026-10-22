from urllib.parse import urlencode
from urllib.request import urlopen
urlopen("https://wiki.example/bin/get/Main/SolrSearch?"+urlencode({"media":"rss","text":"plain text"})).read()
