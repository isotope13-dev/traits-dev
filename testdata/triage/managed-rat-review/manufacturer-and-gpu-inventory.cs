using System;
using System.Management;
class Probe {
  public static bool IsVirtualMachine() {
    foreach (ManagementObject item in new ManagementObjectSearcher(
        "SELECT * FROM Win32_ComputerSystem").Get()) {
      if (item["Manufacturer"].ToString().Contains("VMware") ||
          item["Model"].ToString().Contains("VirtualBox")) return true;
    }
    return false;
  }
  public static void InventoryGpu() {
    foreach (ManagementObject item in new ManagementObjectSearcher(
        "SELECT * FROM Win32_VideoController").Get())
      Console.WriteLine(item["Name"]);
  }
}
