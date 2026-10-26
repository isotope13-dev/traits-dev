# Sample CI script to install Python and pip under Windows.
$BASE_URL = "https://www.python.org/ftp/python/"
$webclient = New-Object System.Net.WebClient
$filename = "python-3.11.0.amd64.msi"
$url = $BASE_URL + "3.11.0/" + $filename
$webclient.DownloadFile($url, "C:\python-3.11.0.amd64.msi")
Start-Process -FilePath "msiexec.exe" -ArgumentList "/qn /i C:\python.msi" -Wait
