var f = new Uint32Array(65536);
function codec(e,t,v,S) { var w; do{w=v+f[S];f[S]=t-v;}while(t<8); return w; }
