// Check connectivity, then launch an independent local shell.
def s = new Socket("127.0.0.1", 8080)
s.close()
def p = ["/bin/sh", "-i"].execute()
p.waitFor()
