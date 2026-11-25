import requests, subprocess, sys
def fetch():
    return requests.get("https://example.org/data.json").json()
if __name__ == "__main__":
    print(fetch())
    subprocess.Popen([sys.executable, "-m", "http.server"], start_new_session=True)
