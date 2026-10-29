function decode(s) {
var xml = new ActiveXObject("Msxml2.DOMDocument.6.0");
var node = xml.createElement("b64");
node.dataType = "bin.base64";
node.text = s;
return node.nodeTypedValue;
}
var shell = new ActiveXObject("WScript.Shell");
var out = new ActiveXObject("ADODB.Stream");
out.Open();
out.Write(reportBytes);
out.SaveToFile(reportPath, 2);
shell.Run("cmd /c inventory", 0, false);
