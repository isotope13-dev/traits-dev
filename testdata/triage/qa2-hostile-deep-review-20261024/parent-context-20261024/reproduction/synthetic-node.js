var events = [], timers = [], module = {exports:{}}, exports = module.exports;
var global = globalThis, __dirname = 'C:\\Synthetic\\resources\\app.asar';
function record(kind,args) { if(events.length >= 250) throw Error('Event limit'); events.push({kind:kind,args:Array.prototype.slice.call(args)}); }
var console = {log:function(){},warn:function(){},error:function(){}};
var process = {env:{APPDATA:'C:\\Synthetic\\AppData',LOCALAPPDATA:'C:\\Synthetic\\Local',TEMP:'C:\\Synthetic\\Temp',COMPUTERNAME:'synthetic-host',PROCESSOR_IDENTIFIER:'synthetic-cpu',PROCESSOR_ARCHITECTURE:'x64',NUMBER_OF_PROCESSORS:'4',SystemDrive:'C:'},execPath:'C:\\Synthetic\\Spacey.exe',on:function(){},exit:function(){record('process.exit',arguments);}};
function setTimeout(fn,ms){record('setTimeout',[ms]);timers.push(fn);return 1;}
function setInterval(fn,ms){record('setInterval',[ms]);return 2;}
function clearInterval(){} function clearTimeout(){}
var fakeAxios = {create:function(){record('axios.create',arguments);return fakeAxios;},get:function(url){record('http.get',arguments);if(url==='https://www.google.com')return Promise.resolve({data:'synthetic-connectivity'});if(url==='')return Promise.reject(Error('Synthetic empty URL'));return Promise.resolve({data:syntheticResponse});}};
function pipe(){return {on:function(){return this;}};}
var fakeChild = {exec:function(command){record('child.exec',arguments);return {stdout:'',stderr:''};},spawn:function(file,args){record('child.spawn',arguments);return {stdout:pipe(),stderr:pipe(),on:function(name,fn){if(name==='exit')fn(0);return this;}};}};
var fakeFS = {writeFileSync:function(){record('fs.writeFileSync',arguments);},existsSync:function(){return true;},mkdirSync:function(){record('fs.mkdirSync',arguments);},readdirSync:function(){return ['synthetic.exe','synthetic.ps1','synthetic.bat','synthetic.msi','ignore.txt'];},statSync:function(){return {isFile:function(){return true;}};}};
var fakePath = {join:function(){return Array.prototype.join.call(arguments,'\\');},extname:function(s){return s.slice(s.lastIndexOf('.'));}};
var fakeOS = {totalmem:function(){return 8*1024*1024*1024;},version:function(){return 'Synthetic OS';},uptime:function(){return 3600;},homedir:function(){return 'C:\\Users\\synthetic-user';},hostname:function(){return 'synthetic-host';},userInfo:function(){return {username:syntheticUsername};},type:function(){return 'Windows_NT';},arch:function(){return 'x64';},release:function(){return '10.synthetic';}};
var fakeSI = {graphics:function(){return Promise.resolve({controllers:[{model:'synthetic-gpu'}],displays:[{resolutionX:1920,resolutionY:1080}]});},osInfo:function(){return Promise.resolve({platform:'win32',distro:'Synthetic Windows'});},system:function(){return Promise.resolve({virtual:false});}};
var fakeZip = {extract:function(){record('zip.extract',arguments);return Promise.resolve();}};
var fakeHTTPS = {Agent:function(options){record('https.Agent',[options]);}};
function require(name){
 record('require',arguments);
 if(name==='axios')return fakeAxios;
 if(name==='https')return fakeHTTPS;
 if(name==='zlib')return {};
 if(name==='fs')return fakeFS;
 if(name==='os')return fakeOS;
 if(name==='child_process')return fakeChild;
 if(name==='zip-lib')return fakeZip;
 if(name==='path')return fakePath;
 if(name==='systeminformation')return fakeSI;
 if(name==='./configuration.js'){
  var m={exports:{}};
  new Function('module','exports','require',configurationSource)(m,m.exports,require);
  return m.exports;
 }
 throw Error('Blocked synthetic module '+name);
}
