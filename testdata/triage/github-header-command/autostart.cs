using Microsoft.Win32;
class Autostart {
 void Register(string exe) {
 Registry.SetValue(@"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "Updater", exe);
 }
}
