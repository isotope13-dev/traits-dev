# Mentioning kubernetes and GCE in an arbitrary script must NOT downgrade Defender disable.
Set-MpPreference -DisableRealtimeMonitoring $true
