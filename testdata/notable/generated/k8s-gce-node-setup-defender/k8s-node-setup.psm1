# Copyright 2019 The Kubernetes Authors.
# Library for configuring Kubernetes Windows nodes on GCE.
# https://github.com/kubernetes/kubernetes/issues/75148
function Disable-WindowsDefender {
  if ((Get-WindowsFeature -Name 'Windows-Defender').Installed) {
    Set-MpPreference -DisableRealtimeMonitoring $true
  }
}
