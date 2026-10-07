window.onbeforeunload = null;
function reload() { location.reload(); }
function render(items) { var i=0; while(true) { if(i < items.length) {} else { break; } console.log(items[i++]); } }
localStorage.setItem('theme', 'dark');
