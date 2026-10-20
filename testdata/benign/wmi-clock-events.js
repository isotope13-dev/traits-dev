var service = GetObject("winmgmts:\\\\.\\root\\cimv2");
var clock = service.ExecNotificationQuery(
  "SELECT * FROM __InstanceModificationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_LocalTime'");
clock.NextEvent();
