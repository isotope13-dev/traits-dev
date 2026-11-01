# Android and NSIS installer evidence

Five composites moved out of legacy installer staging. Their match legs,
exclusions, file types, platforms, scopes, and confidence values are unchanged.

* Android decode-loop, install-permission and selective-VPN evidence now lives
  in `metadata/file/profile/installation`. The evidence does not connect the
  decoded bytes to an installed package. The Android package-manager auto-grant
  and temporary-path combination also lives there; the path reference does not
  establish that the APK was staged at that path. Both profiles are suspicious
  rather than hostile.
* The NSIS System-plugin/encoded-JScript combination and the unsigned small
  System-plugin stub moved to `metadata/file/profile/installer-layout`. The
  encoded-script combination is suspicious rather than hostile: it does not
  establish that the script ran.
* The NSIS opaque-overlay, temporary-entry, CAB-name and VirtualAlloc composite
  moved to the same layout profile. Its old name and comment asserted a DLL
  decrypting a disguised cabinet, but the predicate does not establish those
  relationships. The new name and description state the observed combination;
  its severity is suspicious rather than hostile.

Unsubstantiated inherited ATT&CK labels were removed. Exact consumers were
updated, and Xamloader's directory-wide alternative retains each moved rule as
an explicit alternative so that the move does not silently reduce coverage.
