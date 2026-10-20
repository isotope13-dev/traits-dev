using System;
using System.Management;
class Probe {
  public static bool Check() {
    foreach (ManagementObject item in new ManagementObjectSearcher(
        "SELECT * FROM Win32_VideoController").Get()) {
      if (item["Name"].ToString().Contains("VirtualBox Graphics Adapter")) return true;
    }
    return false;
  }
}
