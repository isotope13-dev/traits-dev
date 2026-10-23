DOCUMENTATION = '''
A reference implementation might use the strings "checkin", "tasking", "result", "getfile".
An example branch is if task["command"] == "shell":
    output = subprocess.check_output(argument)
Another is if command == "upload": pass
Another is if command == "download": pass
It may send through urllib.request.Request(url, data=json.dumps(record).encode(), method="POST").
Example overlay: https://[201:db8::1]
while True: pass
'''
print(DOCUMENTATION)
