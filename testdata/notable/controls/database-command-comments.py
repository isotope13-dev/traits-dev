import json
# sudo kill -9 $(sudo lsof -ti:5432); sudo rm -rf /var/lib/postgresql/*/main
print(json.dumps({'status': 'ready'}))
