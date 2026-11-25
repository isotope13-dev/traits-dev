import dns.resolver, subprocess
D="example.com"
def spf(label):
    ans = dns.resolver.resolve(f"{label}.{D}", "TXT")
    return ans
while True:
    print(subprocess.check_output("hostname", shell=True))
    break
