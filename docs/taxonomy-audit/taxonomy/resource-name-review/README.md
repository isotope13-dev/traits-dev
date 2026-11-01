# Resource name and identity review

The last 16 rules in legacy `staging/resource` were moved, retiring the
category. Their match conditions, scopes and confidence are preserved; unknown
resource strings and a byte pattern are components rather than claims of
specific encrypted resources or decoy captions. The unusual Delphi marker
combination remains suspicious, and the API-hash and embedded-PE combination
retains its likely module-loading objective.

The resource identity directory had 85 direct rules. Seventeen generic resource
text, representation and table observations moved to their respective subjects,
leaving 68. The new `resource/label` leaf contains generic tokens, names and
captions observed within `.rsrc`; it does not assert that the strings are
resource-directory names or verified product identities. The split preserves
all effective match definitions and references.

The split exposed an expanded downgrade of 260 rules on
`encoded-version-resource-config` (limit 256). Its broad
`metadata/binary/resource/` selector contained `pe-version-resource`, a
required positive leg of `anomalous-version-resource`, which the same rule
requires. Thus every positive match also triggered that downgrade. The broad
selector was removed; the narrower installer, Bitdefender identity and import
count downgrades remain. No suppression width limit was changed.

| Former legacy ID | Destination ID | Criticality |
|---|---|---|
| `rsrc-on-demand-route-helper-name` | `metadata/binary/resource/label::on-demand-route-helper-dll-text` | notable |
| `rsrc-startupscan-dll-name` | `metadata/binary/resource/label::startupscan-dll-text` | notable |
| `rsrc-ztdnsapi-dll-name` | `metadata/binary/resource/label::ztdnsapi-dll-text` | notable |
| `rsrc-deviceassociation-dll-name` | `metadata/binary/resource/label::deviceassociation-dll-text` | notable |
| `rsrc-security-integrity-dll-name` | `metadata/binary/resource/label::security-integrity-dll-text` | notable |
| `springfield-armory-version-string` | `metadata/binary/resource/label::springfield-armory-text` | notable |
| `tr-configuration-service-string` | `metadata/binary/resource/label::tr-configuration-service-text` | notable |
| `tjertier6-resource-name` | `metadata/binary/resource/label::tjertier6-resource-text` | component |
| `tke5rhiwr-form-resource` | `metadata/binary/resource/label::tke5rhiwr-resource-text` | component |
| `tke5rhiwr-form-create-caption` | `metadata/binary/resource/label::3rqefdas-resource-text` | component |
| `tjertier6-interleaved-resource-header` | `metadata/binary/resource/representation::interleaved-resource-header-pattern` | component |
| `windows-component-resource-name-cluster` | `metadata/binary/resource/label::resource-dll-name-cluster` | component |
| `springfield-configuration-version-claim` | `metadata/binary/resource/label::springfield-configuration-text-pair` | component |
| `windows-component-resource-carrier` | `metadata/file/profile/pe-loader-context::unsigned-resource-pe-dll-name-clues` | suspicious |
| `tjertier6-delphi-resource-loader` | `metadata/file/profile/pe-loader-context::delphi-resource-marker-api-clues` | suspicious |
| `api-hashed-component-resource-loader` | `objectives/execution/payload/module-load::api-hash-resource-pe-loader-clues` | hostile |

| Former identity ID | Destination |
|---|---|
| `reginst-resource-label` | `metadata/binary/resource/label::reginst-resource-label` |
| `image-resource-label` | `metadata/binary/resource/label::image-resource-label` |
| `setup-exe-resource-name` | `metadata/binary/resource/label::setup-exe-resource-name` |
| `updater-exe-resource-string` | `metadata/binary/resource/label::updater-exe-resource-string` |
| `updater-resource-string` | `metadata/binary/resource/label::updater-resource-string` |
| `updater-role-label-text` | `metadata/binary/resource/label::updater-role-label-text` |
| `system-configuration-utility` | `metadata/binary/resource/label::system-configuration-utility` |
| `about-test-title` | `metadata/binary/resource/label::about-test-title` |
| `test-version-title` | `metadata/binary/resource/label::test-version-title` |
| `test-branding-cluster` | `metadata/binary/resource/label::test-branding-cluster` |
| `short-titlecase-resource-words` | `metadata/binary/resource/representation::short-titlecase-resource-words` |
| `pe-resource-opaque-token` | `metadata/binary/resource/representation::pe-resource-opaque-token` |
| `fzkxj-resource-text` | `metadata/binary/resource/representation::fzkxj-resource-text` |
| `script-datum-resource-text` | `metadata/binary/resource/representation::script-datum-resource-text` |
| `wide-settings-resource-name` | `metadata/binary/resource/table::wide-settings-resource-name` |
| `pe-single-version-resource` | `metadata/binary/resource/table::pe-single-version-resource` |
| `pe-no-version-info-resource` | `metadata/binary/resource/table::pe-no-version-info-resource` |
