"""Run traced source with inert HTTP/auth modules in QuickJS; no network."""
import pathlib,json,quickjs
p=pathlib.Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/review-9f-e1-eb');root=pathlib.Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/extract/e1804b/package/lib/lib');c=quickjs.Context();c.set_memory_limit(64*1024*1024);c.set_time_limit(1)
c.eval('''
const requests=[],actions=[],storage=new Map();
const console={error(){},warn(){},log(){}};
const localStorage={getItem:k=>storage.get(k),setItem:(k,v)=>storage.set(k,v)};
const crypto={getRandomValues:a=>a.fill(42)};
class HTTP {
 setDataSerializer(){}
 async get(url){requests.push({method:'GET',url});return url.includes('instagram.com')?{headers:{'set-cookie':['csrftoken=fixture']}}:{data:JSON.stringify({users:['operator-target'],posts:['operator-post']})};}
 async post(url,body,headers){requests.push({method:'POST',url,body,headers});return {headers:{'set-cookie':['sessionid=fixture']},data:JSON.stringify({logged_in_user:{pk:42}})};}
}
const dependencies={
 '@awesome-cordova-plugins/http/ngx':{HTTP},uuid:{v4:()=> 'fixture-uuid'},
 './cookies.service':{CookiesService:class{formatCookie(){return 'sessionid=fixture'}getEarliestExpireDate(){return 'tomorrow'}}},
 '../config':{config:{loginHeader:'fixture-UA'}},
 './login.bloks':{BloksLoginService:class{async login(){return {authorization:'Bearer fixture-session',userId:'42'}}}},
 './client.service':{InstaService:class{async follow(u,h){actions.push({action:'follow',target:u,authorization:h.Authorization})}async like(u,h){actions.push({action:'like',target:u,authorization:h.Authorization})}}}
};
function require(n){if(n in dependencies)return dependencies[n];throw Error('Blocked module '+n);}
let handler={},loginModule={},error=null;
''')
for file,export in [('handler.js','handler'),('login.service.js','loginModule')]:
 c.eval('(function(exports,require){\n'+(root/file).read_text()+'\n})('+export+',require);')
c.eval("handler.getCookies('fixture-user','fixture-password',true).catch(e=>error=String(e));")
while c.execute_pending_job():pass
assert c.eval('error') is None
requests=json.loads(c.eval('JSON.stringify(requests)'));leak=next(r for r in requests if '/check' in r['url']);assert leak['body']['data']['pass']=='fixture-password';assert 'fixture-password' in leak['body']['data']['body'];assert 'logged_in_user' in leak['body']['data']['data']
c.eval("new loginModule.LoginService().login('fixture-user','fixture-password').catch(e=>error=String(e));")
while c.execute_pending_job():pass
assert c.eval('error') is None
actions=json.loads(c.eval('JSON.stringify(actions)'));assert len(actions)==2;assert all(a['authorization']=='Bearer fixture-session' for a in actions)
(p/'npm.effects.json').write_text(c.eval('JSON.stringify({requests,actions},null,2)')+'\n');print('Verified password leak and remote follow/like activation with inert stubs')
