// Classic FSO log rotation helper (Windows admin scripting).
var fso = new ActiveXObject("Scripting.FileSystemObject");
var logFile = fso.CreateTextFile("C:\\Logs\\app.log", true);
logFile.WriteLine("started");
logFile.Close();
