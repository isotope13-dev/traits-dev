#!/usr/bin/env python3
"""Execute originals only with imports, file writes, forks and HTTP replaced."""
import argparse
import builtins
import io
import json
from pathlib import Path
from types import SimpleNamespace

parser = argparse.ArgumentParser()
parser.add_argument('--samples', type=Path, required=True)
base = parser.parse_args().samples
trace = []
class StopLoop(BaseException):
    pass
class Response:
    def __init__(self, body): self.body = body
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self): return self.body

def urlopen(url, **kwargs):
    trace.append(['urlopen', url, kwargs])
    return Response(b'controller.invalid\nignored.invalid' if 'raw.githubusercontent' in url else b'pass')
def opened(path, mode):
    trace.append(['open',path,mode]); return io.StringIO()
def sleeping(seconds):
    trace.append(['sleep',seconds]); raise StopLoop()
def compiled(source, filename, mode):
    trace.append(['compile',source,filename,mode]); return compile(source,filename,mode)
def executed(code, globals):
    trace.append(['exec',code.co_filename,globals]); builtins.exec(code,globals)

os_stub = SimpleNamespace(fork=lambda: 1, setsid=lambda:trace.append(['setsid']), path=SimpleNamespace(exists=lambda _:False))
request = SimpleNamespace(urlopen=urlopen)
imports = {'os':os_stub, 'time':SimpleNamespace(sleep=sleeping), 'urllib.request':SimpleNamespace(request=request)}
custom = dict(vars(builtins), __import__=lambda name,*a,**k:imports[name], open=opened, compile=compiled, exec=executed)
namespace = {'__name__':'sitecustomize','__builtins__':custom}
builtins.exec(compile((base/'5c9d66286ab2/sitecustomize-urllib-variant.py').read_text(),'original-loader','exec'),namespace)
assert trace == [['open','/tmp/.site_loader.lock','w']]
os_stub.fork = lambda: 0
try: namespace['_daemon']()
except StopLoop: pass
assert [t[1] for t in trace if t[0]=='urlopen'] == ['https://raw.githubusercontent.com/someone/cfg/main/host.txt','http://controller.invalid/payload']
assert any(t[0]=='setsid' for t in trace)
assert any(t[0]=='exec' and t[1]=='<remote>' for t in trace)
assert trace[-1] == ['sleep',3600]
# Remove the interpreter-added builtins dictionary from the saved trace.
for t in trace:
    if t[0]=='exec': t[2] = {'__name__':t[2]['__name__']}

calls=[]
def post(endpoint, data, headers, verify):
    calls.append([endpoint,dict(data),headers,verify])
    hit = data['username']=='alice' and data['password']=='candidate2'
    return SimpleNamespace(json=lambda:{'access_token':'test-access','refresh_token':'test-refresh'} if hit else {'error':'invalid_grant'})
imports={'os':SimpleNamespace(environ={}), 'random':SimpleNamespace(uniform=lambda a,b:0,randint=lambda a,b:30), 'time':SimpleNamespace(sleep=lambda s:None), 'requests':SimpleNamespace(post=post)}
custom=dict(vars(builtins), __import__=lambda name,*a,**k:imports[name], print=lambda *a:None)
namespace={'__name__':'review','__builtins__':custom}
builtins.exec(compile((base/'7b6c9a664063/entra_spray.py').read_text(),'original-spray','exec'),namespace)
hits=namespace['spray'](['alice','bob'],['candidate1','candidate2'],namespace['TOKEN_URL'])
assert [(r[1]['password'],r[1]['username']) for r in calls] == [('candidate1','alice'),('candidate1','bob'),('candidate2','alice'),('candidate2','bob')]
assert hits == [('alice','candidate2','test-refresh')]
assert all(r[3] is False for r in calls)
print(json.dumps({'loader_trace':trace,'spray_calls':calls,'spray_retained':hits},indent=2))
