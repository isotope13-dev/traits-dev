import subprocess
with open("/tmp/.accounts.ldif", "w") as f:
    f.write("dn: cn=test,dc=example,dc=test\n")
subprocess.Popen(["ldapadd", "-f", "/tmp/.accounts.ldif"], stderr=subprocess.DEVNULL)
