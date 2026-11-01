$script = "C:\ProgramData\stage.au3"
schtasks.exe /Create /SC DAILY /TN "Daily report" /TR "C:\Program Files\Reports\report.exe"
