const platform=()=>1, release=()=>2, gzip=()=>3, promisify=(f:Function)=>f; platform(); release(); promisify(gzip);
