var query = "SELECT * FROM __InstanceModificationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_LocalTime'";
var service = GetObject("winmgmts:\\\\.\\root\\cimv2");
service.ExecQuery("SELECT * FROM Win32_LocalTime");
