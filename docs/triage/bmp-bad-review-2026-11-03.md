# BMP mislabeled-bad review

Completed: 40 bad artifacts. Most are executable or archive containers with bitmap-named members; the full container was evaluated. Both scanners completed full-artifact scans, and validation passed after the final trait changes.

- `888cfc87b44024c48eed794cc9d6dea9f6ae0cc3468dee940495e839a12ee0db` — **bad** — A BMP contains an obfuscated script that reconstructs and launches an executable. Both scanners detected the combined script and execution clues; validation passed and Hopper confirmed bad.
- `3046d9e6d364bf2dbb3d67251919fa792769c87dbe2a36cb76faf5217fe32137` — **bad** — This self-extracting archive contains a VBScript that launches a contained executable while hiding the short launcher among extensive random comment padding. The new trait joins comment structure, entropy, digit distribution, shell creation and executable invocation; both scanners matched the extracted script, cleave matched it in the archive, and three negative controls and full validation passed. Hopper confirmed bad.
- The following nine artifacts also contain a random-comment-padded VBScript launcher for a bundled executable or PIF: `69aefba0bddbb8f38a5913d51d61936647e4dfccd4d561f51519f5a35d7f834c`, `65f6a568a39f5285acc4fd58563be987f6a128165ae0b89cffc038a26f4e54b6`, `8ff2d981a86955231e1ba93163f8a5fcbcf83b46980824476b7137d1caf2e935`, `e8ac69b242f87152457399a019803c892209200c3951f6a0efc05cde5dd5edf5`, `b2064c9af50ac66d478011d5c176ff5329f32f4c3e20aadd0c78950d7e078849`, `ef91f207b54cb16c1178b0fe801c2fafd5ee101c527c07225fe453dfa63428d3`, `0cc115545b035f30597cb2490f47f1f8c60ee502bb908f4cefdf8f84a662a382`, `9530267408a020ad51d1152af9d09129f78ac294080ba334cc6843a9a44d07e6`, and `eaf94fe4abeb08e2fc01bc00fe2768ce691e2dc0931bb53daa17f05466debab8` — **bad**. Both full-artifact rescans detected the combined obfuscation and launcher facts; controls and full validation passed, and Hopper confirmed the labels. At least the `65f6` script contains a malformed quote, so the finding indicates hostile launcher code rather than confirmed successful execution.
- `b78996718e94fe9cf9cc228f474b774fd7bd54133762d183ba2e6c141b3a218a`, `13449784267e8b9f277e7aa2fdacecadfa3ad1843bf750190963b69b3b590c8f` and `be362fc466bdf33024f36b55c40b191db842063f2183ba752d4a0c1e73115ffa` — **bad** — Related padded launchers pass a bundled PIF and data file in a single string. Both scanners detected the extracted scripts and their containers after extending the same combined rule. Three negative controls and full validation passed; Hopper confirmed bad.

The following 22 artifacts are **bad**: both scanners expose a common combination of a silent SFX setup, a legacy executable, at least 20-fold expansion, at least ten members, multiple executable-looking members and a high-entropy executable overlay. Inspection of every SFX configuration confirmed it silently launches a randomly named PIF with a separately named data file. A representative data member expanded to 81.6 MB and was padded with repeated high-entropy content. These are strong combined signs of deliberately obscured execution; the full behavior of the PIF and data has not been recovered. Hopper confirmed all labels. An attempted composite could not join the facts across the container layers, so this aggregate detection gap remains; no engine change was made.

- `d2cae38f605d546b4898e0cc7e0a641c0eca70d57b1cd4a0ee255e421597f580`
- `1f9093429b52b5ef27a07ff7aa73890a15373c591f40729f406fc22cb26e6112`
- `3d70a8eff056fc33703bf11e6fade74fa83bad86dc4014768cc8725e50a6e396`
- `1acf4f64dbce46e70553494cf02959634528477066cc736e3f49df3bb6253923`
- `8b5143b685f294c156d2d0b8d3e64eb4874f82dc0c8a40ab5bd8d5dc02f61fe8`
- `5a40f4c70cc4bf22204a97d56b5e2a43a32cb2a87bc3a0ff3eba286c69037b9e`
- `d38185c3dd6800479186992141c2b6c804e06efe4fdc16b35b804cc987a5ba45`
- `e1283a5b801014d33c4541d22f8069e6c7003073404cbcbde501a32cd39aac74`
- `fb0d1b0c62204ebfb2e04bcc607e562f398bf0cd40a275ace02ca34bed1d355d`
- `a9d20de79009e68c2547b41762e1a48b172aa41ed5124bb295d58dfac1c695d4`
- `2d2f62269797be7ef763ac2da37e4c190381cfba8798e92e73ee9aa2084386f1`
- `98040fcdb39c2cccaae5670033e20aaf0e49671081c9b06ae3c664057797a05d`
- `63b45db1a34b47cfe915e7ae7fdd80d25b216259eb8a49f950d54d6b985155ec`
- `1fc373d38486f7472f73f5695f5ed8de9b32980cef2b1e493ce763cd4758545f`
- `9ee1ed01fe26af330a114bc5d39fdfb3a6357a75b8091a234d115bf2230256c3`
- `cef25f5a97e0ef3ce46c5854adb423091ee866ae50fedfd408265b29e85e840b`
- `5843b2cf0911e1e3ee1ad03e232c2d9f44a0c48806ff62eb0af25ade8695b3b9`
- `1678611ad4996f718c0a8998ce194dfe117bf47529c4ccad51a6816ecf4f1bb4`
- `0418e3df48284da14ab4d183c6d5d6ec3f37e3bd2b7be5439840d8409e620c32`
- `28aa8ec808487bfc4089e22b1d14ddb6c85a490a27f95dba52248bf4ad46e365`
- `bd0d664991e33a8e4771a5437df9e937036c827e04f49e9c55b9e7fb7a01912e`
- `1a4d341543505d9f93c530bbacc6a55218d016019d4be4b0443b43ecb6fa0452`

- `fceef2124ae276c4eeebdeb15194e3aebe3cdbbcd58d7d4e24f5d102b17c4845` and `273fc22bc707da117959cd5088c60c3052962fe183a51a2b8a6c66820723cbfd` — **bad** — Both have the same silent SFX configuration launching a randomly named PIF with a data argument and expansion-heavy decoy archive, but did not meet every member-count condition used to select the preceding group. Hopper confirmed bad.
- `cea6201673a31d0b426c47886dbd386da13c65593b8fbde71fd70cba51272a1e` — **bad** — A payment-advice-named executable in a ZIP silently extracts and starts encoded VBScript, with an executable disguised as a BMP and an expansion-heavy decoy archive. Both scanners detected the SFX launcher; Hopper confirmed bad.
- `5d03fd083b626a5516194d5e94576349100c9c98ca7d6845642ed9579980ca58` — **bad** — An SFX with an embedded AutoIt executable, a text file named as an icon, dozens of decoys and a 105 MB member compressed to 85 KB displays related deliberate payload-hiding and inflation. The embedded executable's full behavior and SFX launch configuration were not recovered. Both scans found the archive anomalies; Hopper confirmed bad.
