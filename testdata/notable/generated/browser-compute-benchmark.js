
const started = performance.now();
for(let j=0;j<1e5;j++)Math.sqrt(j);
console.log(performance.now()-started);
if(navigator.webdriver) console.log('automated');
window.location.replace('/results');
