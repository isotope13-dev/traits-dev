function gy(e, t) {
    return e.replace(/[a-zA-Z]/g, (r) => {
        let n = r <= "Z" ? 65 : 97;
        return String.fromCharCode((r.charCodeAt(0) - n + t) % 26 + n)
    })
}
function yy(e, t) {
    let r = gy(e, t),
        n = (26 - t) % 26;
    return `(function(){var _r=0,_s=1,_t=2;try{eval((function(d,k){return d.replace(/[a-zA-Z]/g,function(v){var o=v<="Z"?65:97;return String.fromCharCode((v.charCodeAt(0)-o+k)%26+o)})})([${Array.from(r,(i)=>i.charCodeAt(0)).join(",")}].map(function(x){return String.fromCharCode(x)}).join(""),${n}))}catch(_){}})();`
}
