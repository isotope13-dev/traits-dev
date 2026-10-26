from pathlib import Path
import quickjs,json,sys
p=Path(sys.argv[1])
s=p.read_text();a=s.index('if("undefined"!=typeof window&&/^ru\\b/.test(navigator.language)');b=s.index('SweetAlert.prototype.disableButtons=',a);code=s[a:b]
assert len(code)<1000
results=[]
for lang,host,age in [('ru-RU','test.ru',None),('ru-RU','test.ru',3),('ru-RU','test.ru',3.01),('ru','test.su',4),('ru-BY','test.by',4),('ru-RU','test.xn--p1ai',4),('en-US','test.ru',4),('ru-RU','test.com',4),('ru-RU','test.ru.example.com',4)]:
 c=quickjs.Context();c.eval('''var actions=[];var window={};var now=1800000000000;
 var NativeDate=Date;Date=class extends NativeDate{constructor(...args){super(...(args.length?args:[now]))}};
 var document={body:{style:{},appendChild(e){actions.push(['append',e.src,e.loop])}},createElement(tag){actions.push(['create',tag]);return {play(){actions.push(['play']);return {catch(){}}}}}};
 function setTimeout(cb,ms){actions.push(['timeout',ms]);cb()}
 ''')
 c.eval('var navigator='+json.dumps({'language':lang})+';var location='+json.dumps({'host':host})+';')
 timestamp=c.eval('new Date(now-'+str((age or 0)*864e5)+').toISOString()') if age is not None else None
 c.eval('var stored='+json.dumps(timestamp)+';var localStorage={getItem(k){actions.push(["get",k]);return stored},setItem(k,v){actions.push(["set",k,v])}};')
 c.eval(code);res=json.loads(c.eval('JSON.stringify({pointerEvents:document.body.style.pointerEvents||null,actions:actions})'))
 blocked=bool(res['pointerEvents']);expected=age is not None and age>3 and lang.startswith('ru') and host.split('.')[-1] in ['ru','su','by','xn--p1ai']
 assert blocked==expected,(lang,host,age,res)
 results.append({'language':lang,'host':host,'age_days':age,**res})
print(json.dumps(results,indent=2))

