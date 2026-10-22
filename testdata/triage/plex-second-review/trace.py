"""Trace selected source functions with a recording HTTP transport, no sockets.

Only explicitly selected function ASTs are compiled. Never import the sample
module, start listeners, run compilers, or launch shell payloads.
"""
import ast, json, re, sys, types
from pathlib import Path
import urllib.parse, urllib.request, urllib.error
path=Path(sys.argv[1]);tree=ast.parse(path.read_text())
names={'hget','preq','steal_owner_token','revshell_cmd','transcode_params'}
selected=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in names]
assert len(selected)==len(names)
requests=[]
class Response:
    status=200
    def read(self):return b''
def urlopen(request,**kwargs):
    requests.append({'url':request.full_url,'method':request.get_method(),'headers':dict(request.header_items())})
    return Response()
http=types.SimpleNamespace(parse=urllib.parse,error=urllib.error,request=types.SimpleNamespace(Request=urllib.request.Request,urlopen=urlopen))
class Thread:
    def __init__(self,target=None,**kwargs):self.target=target
    def start(self):
        if self.target:self.target()
class Catcher:
    def __init__(self,*args):self.token='local-INERT-TEST-VALUE';self.got=types.SimpleNamespace(wait=lambda **kwargs:None)
    def start(self):pass
    def stop(self):pass
ns={'urllib':http,'time':types.SimpleNamespace(sleep=lambda _:None,time=lambda:100000),'threading':types.SimpleNamespace(Thread=Thread),'TokenCatcher':Catcher}
exec(compile(ast.Module(body=selected,type_ignores=[]),str(path),'exec'),ns)
args=types.SimpleNamespace(target='target.example.test:32400',token_port=8952,attacker_host='127.0.0.1.203-0-113-9.example.test',plex_port=32400,junk_token='TOTALLY_INVALID_JUNK',wait=0)
assert ns['steal_owner_token'](args)=='local-INERT-TEST-VALUE'
assert len(requests)==3
query=urllib.parse.parse_qs(urllib.parse.urlsplit(requests[1]['url']).query)
protocol=query['protocol'][0]
identifier=urllib.parse.parse_qs(urllib.parse.urlsplit(protocol).query)['identifier'][0]
assert protocol.startswith('http://127.0.0.1:32400/system/agents/')
assert 'GetResultFromNetwork?url=http://127.0.0.1.203-' in identifier
print(json.dumps({'recorded_requests':requests,'decoded_protocol':protocol,'decoded_identifier':identifier,'generated_shell_command':ns['revshell_cmd']('203.0.113.9',9001),'transcoder_arguments':ns['transcode_params']('http://carrier.example.test/item.xml','INERT',640,360),'limitations':'Recording transport; fake token; no sample module initialization, network, compiler, or shell execution.'},indent=2))
