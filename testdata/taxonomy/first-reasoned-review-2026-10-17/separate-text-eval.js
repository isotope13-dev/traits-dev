async function text(url) { const response = await fetch(url); return response.text(); }
function runLocal(code) { window["eval"](code); }
