using System.Diagnostics;
class Reminder {
  static void Main() {
    Process.Start("schtasks", "/create /tn \"CalendarReminder\" /tr \"reminder.exe\" /sc onlogon /f");
  }
}
