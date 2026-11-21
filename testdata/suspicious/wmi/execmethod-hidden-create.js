var wmi = new ActiveXObject("WbemScripting.SWbemLocator").ConnectServer(".", "root\\cimv2");
var process = wmi.Get("Win32_Process");
var startup = wmi.Get("Win32_ProcessStartup").SpawnInstance_();
startup.ShowWindow = 0;
var args = process.Methods_.Item("Create").InParameters.SpawnInstance_();
args.ProcessStartupInformation = startup;
args.CommandLine = "notepad.exe";
process.ExecMethod_("Create", args);
