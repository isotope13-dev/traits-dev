var service = GetObject("winmgmts:\\\\.\\root\\cimv2");
var processes = service.ExecNotificationQuery(
  "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_Process'");
processes.NextEvent();
