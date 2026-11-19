import http.client, threading, time, uuid, itertools, sys
TARGET = "ingress-nginx-controller.ingress-nginx.svc.cluster.local"
RATE = 20
PAYLOADS = [
  ("clean", "/?q=hello"),
  ("sqli", "/?id=1%27%20OR%20%271%27%3D%271%27%20UNION%20SELECT%20username,password%20FROM%20users--"),
  ("xss", "/?q=%3Cscript%3Ealert(document.cookie)%3C/script%3E"),
  ("traversal", "/?file=../../../../etc/passwd"),
  ("block-marker", "/?canary=sigsci-custom-block-canary"),
]
cnt = itertools.count()
def one(n):
    kind, path = PAYLOADS[n % len(PAYLOADS)]
    rid = f"{uuid.uuid4().hex[:12]}-{kind}"
    t0 = time.time(); status = "ERR"; err = ""
    try:
        c = http.client.HTTPConnection(TARGET, 80, timeout=3)
        c.request("GET", path, headers={"Host": "echo.local", "X-Request-ID": rid})
        r = c.getresponse(); r.read(); status = r.status; c.close()
    except Exception as e:
        err = type(e).__name__
    print(f"{t0:.6f},{rid},{kind},{status},{(time.time()-t0)*1000:.1f},{err}", flush=True)
print("sent_ts,rid,kind,status,lat_ms,err", flush=True)
nxt = time.time()
while True:
    threading.Thread(target=one, args=(next(cnt),), daemon=True).start()
    nxt += 1.0 / RATE
    time.sleep(max(0, nxt - time.time()))
