import subprocess
import sys

PS_QUERY = r"""
$searcher = [adsisearcher]'(&(objectCategory=person)(objectClass=user)(sAMAccountName=jsmith))'
$searcher.PropertiesToLoad.Add('displayName')
$searcher.FindOne().Properties['displayname'][0]
"""

def main():
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", PS_QUERY],
        capture_output=True, text=True, check=False,
    )
    sys.stdout.write(result.stdout)

if __name__ == "__main__":
    main()
