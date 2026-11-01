# Registry and encoded script review

Twenty-one rules from the two legacy registry/PowerShell staging files were organized by the action or evidence they require. Their matching conditions, scopes, confidence values and references were retained.

- Reading registry data near a ScriptBlock constructor does not prove invocation; a nearby Base64 call, expression text or null-pointer delegate also does not by itself establish a registry-sourced payload. These combinations are suspicious registry profiles.
- Registry path, encoded PowerShell write, invocation syntax, removal targets, Base64 assignment and command text have their own subjects. Office's LicensingNext path is a Microsoft Office observation. Generic registry binary-type and property-or-encoding tests remain components.
- The HTA registry-write, PowerShell-expression and Run combinations remain execution objectives. The encoded batch write plus variable invocation remains a batch execution objective. A RunAs relaunch and separate cleanup clues are a suspicious elevation profile. Encoded-command text and dense lines are an observation, not a proven stager.
- The Office LicensingNext path was removed as an exclusion from the HKCU/Base64 profile: a file may mention that path while a different nearby registry read is relevant. This intentionally broadens matching. The remaining specific source-context exclusions and existing downgrade and proximity gates remain unchanged. Unsupported inherited technique annotations were removed from evidence profiles.
