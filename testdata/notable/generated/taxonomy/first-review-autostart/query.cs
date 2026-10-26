using System.Diagnostics;
class Reminder { static void Main() { Process.Start("schtasks", "/query /tn \"CalendarReminder\""); } }
