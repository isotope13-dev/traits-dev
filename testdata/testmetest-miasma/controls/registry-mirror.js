async function mirror(url,data){let a=await fetch(url,{method:"DELETE"});let b=await fetch(url,{method:"PUT",body:data});return base+"/api/npm/"+repo+"/reindex/";}
