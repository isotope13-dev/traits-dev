Private Declare Function RegSetValueExA Lib "advapi32.dll" (ByVal hKey As Long, ByVal name As String, ByVal reserved As Long, ByVal typ As Long, ByVal data As String, ByVal size As Long) As Long
