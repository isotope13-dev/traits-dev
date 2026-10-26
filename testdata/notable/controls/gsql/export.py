import urllib.request
query = 'CREATE QUERY export_report(FILE destination, STRING value) { PRINT value TO_CSV destination; }'
request = urllib.request.Request('http://localhost:14240/api/gsql-server/gsql/v1/statements', data=query.encode(), method='POST')
