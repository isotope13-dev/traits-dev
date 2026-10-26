ObjC.import('Foundation');
function run(argv) {
  var code = ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(argv[0], $.NSUTF8StringEncoding, null));
  var now = Date.parse('2026-10-24T00:00:00Z');
  function Clock() { return new Date(now); }
  Clock.parse = Date.parse;
  var cases = [
    {name:'first-visit',lang:'ru-RU',host:'example.ru',age:null,block:false,store:true},
    {name:'four-days',lang:'ru-RU',host:'example.ru',age:4,block:true},
    {name:'exact-three-days',lang:'ru-RU',host:'example.ru',age:3,block:false},
    {name:'one-day',lang:'ru-RU',host:'example.ru',age:1,block:false},
    {name:'other-language',lang:'en-US',host:'example.ru',age:4,block:false},
    {name:'other-domain',lang:'ru-RU',host:'example.com',age:4,block:false},
    {name:'belarus',lang:'ru',host:'example.by',age:4,block:true},
    {name:'host-port',lang:'ru-RU',host:'example.ru:8443',age:4,block:false}
  ];
  var results=[];
  cases.forEach(function(c) {
    var queue=[], events=[], audio=null, stored=false;
    var storage={getItem:function(){return c.age===null?null:new Date(now-c.age*864e5).toISOString();},setItem:function(k,v){stored=true;events.push(['storage',k,v]);}};
    var doc={body:{style:{},appendChild:function(a){events.push(['append',a.src]);}},createElement:function(tag){if(tag!=='audio')throw Error('unexpected element');audio={play:function(){events.push(['play']);return {catch:function(){}};}};return audio;}};
    var timer=function(fn,delay){events.push(['timer',delay]);queue.push(fn);};
    Function('window','navigator','location','localStorage','document','setTimeout','Date',code)({}, {language:c.lang}, {host:c.host}, storage,doc,timer,Clock);
    while(queue.length) queue.shift()();
    var blocked=doc.body.style.pointerEvents==='none';
    if(blocked!==c.block || (!!c.store)!==stored || (blocked && (!audio.loop || events.filter(function(e){return e[0]==='play';}).length!==1)))throw Error('failed '+c.name);
    results.push({name:c.name,blocked:blocked,stored:stored,audio:audio?{src:audio.src,loop:audio.loop}:null,events:events});
  });
  return JSON.stringify({method:'Exact bundle statement with inert DOM, storage, clock and timer stubs; no network or full library execution',cases:results},null,2);
}
