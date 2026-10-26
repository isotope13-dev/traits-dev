"""Run only the recovered regional routine with clock/DOM/storage stubs."""
import json
from pathlib import Path
import re
import sys
import quickjs

results = []
for filename in sys.argv[1:]:
    source = Path(filename).read_text()
    start = re.search(r'if\s*\(typeof window\s*<\s*"u"\s*&&', source).start()
    end = re.search(r'localStorage\.setItem\("swal-initiation",\s*`\$\{\w+\}`\);?\s*}', source[start:]).end()
    code = source[start:start+end]
    assert len(code) < 1000
    for language, host, age in [
        ('ru-RU', 'test.ru', None), ('ru-RU', 'test.ru', 3),
        ('ru-RU', 'test.ru', 3.01), ('ru', 'test.su', 4),
        ('ru-BY', 'test.by', 4), ('ru-RU', 'test.xn--p1ai', 4),
        ('en-US', 'test.ru', 4), ('ru-RU', 'test.com', 4),
        ('ru-RU', 'test.ru.example.com', 4), ('russian', 'test.ru', 4),
    ]:
        context = quickjs.Context()
        context.set_time_limit(0.5)
        context.eval('''var actions=[], window={}, now=1800000000000;
var OriginalDate=Date;
Date=class extends OriginalDate {
  constructor(...args){super(...(args.length?args:[now]))}
};
var document={body:{style:{},appendChild(e){actions.push(['append',e.src,e.loop])}},
createElement(tag){actions.push(['create',tag]);return {play(){
 actions.push(['play']);return {catch(){}}
}}}};
function setTimeout(callback,ms){actions.push(['timer',ms]);callback()}
''')
        context.eval('var navigator='+json.dumps({'language': language})+';var location='+json.dumps({'host': host})+';')
        stamp = context.eval('new Date(now-'+str((age or 0)*864e5)+').toISOString()') if age is not None else None
        context.eval('var stored='+json.dumps(stamp)+''';var localStorage={
 getItem(k){actions.push(['get',k]);return stored},
 setItem(k,v){actions.push(['set',k,v])}
};''')
        context.eval(code)
        result = json.loads(context.eval('JSON.stringify({pointerEvents:document.body.style.pointerEvents||null,actions})'))
        expected = age is not None and age > 3 and language in ['ru-RU', 'ru', 'ru-BY'] and host in ['test.ru','test.su','test.by','test.xn--p1ai']
        assert (result['pointerEvents'] == 'none') == expected, result
        results.append({'member': Path(filename).name, 'offset': start, 'length': len(code),
                        'language': language, 'host': host, 'age_days': age, **result})
print(json.dumps(results, indent=2))
