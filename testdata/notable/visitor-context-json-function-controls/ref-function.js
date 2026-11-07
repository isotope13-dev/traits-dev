// templating: referrer shown, templates compiled
var tpl = JSON.parse(document.getElementById("tpl").textContent);
document.getElementById("from").textContent = document.referrer;
var render = new Function(tpl[0])();
