var shell = new ActiveXObject('WScript.Shell');
var shortcut = shell.CreateShortcut('C:\\Users\\user\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\app.lnk');
shortcut.TargetPath = 'C:\\Program Files\\App\\app.exe';
shortcut.Save();
