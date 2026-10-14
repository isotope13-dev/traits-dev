Companion-app permissions are declared capabilities, not spyware
==================================================================

`android-sensitive-access-permissions` fired on the OpenClaw Android
companion app, whose mic/camera/location/contacts/calendar/SMS permissions
are its documented capabilities (voice, camera, SMS relay, calendar). The
composite already suppresses known-good vendors (phonesky, smsforwarder,
expo); the existing `openclaw-android-source-tree` identity (source paths
under `apps/android/.../ai/openclaw/`) is now wired in the same way, plus
a member-visible `openclaw-android-theme-reference` marker, because
archive-layout traits cannot be seen from a member manifest entry.

Run `python3 testdata/android-companion-permissions/check.py
<scratch-directory>`. `flashlight-spyware-positive.zip` (same permission
set, unrelated package and theme) must report the trait;
`companion-app-negative.zip` must report no suspicious trait.
