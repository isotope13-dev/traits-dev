$lock = [System.Threading.Mutex]::new($false, 'Global\{6E1963E4-3155-4F60-A51A-624D4CA12092}')
$lock.ReleaseMutex()
