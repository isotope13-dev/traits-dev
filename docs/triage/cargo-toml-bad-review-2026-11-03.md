# Cargo manifest mislabeled-bad review

Review completed: 27 snapshot artifacts.

- `5936a12a6d71b18e6a89f2141eabe271f3a0fb8571b5089a58260e9fee3cb3df` — **good** — A second Sapling source snapshot. Both scanners found no hostile content in the source archive; the remaining suspicious hostname finding is a certificate-validation test. Atom also reported hostile findings in fetched registry and third-party package records despite `--follow none`; those records are separate from this archive. Full validation passed and Hopper moved the sample to good.

- `43928abe301f0794930a0a956a5d995f4f4852c8f175fe7952de083adaac0e49` — **good** — Sapling source with a certificate-validation test containing a NUL-bearing hostname. Cleave found no hostile content; Atom additionally attributed security holds on `isl-server` and `reviewstack` to manifests that resolve those exact versions to local workspace packages. The manifest-only security-hold finding now remains suspicious instead of declaring the manifest hostile; an eight-member workspace control confirms the changed severity. Atom also included fetched registry and package records despite `--follow none`, which are separate from the source archive. Full validation passed and Hopper confirmed good.

- `918935d7e401e70ac801125f94185b62b0afe209fef5748ffb500c7cfdb1a1fe` — **bad** — This agent source archive includes a model-jailbreak racing tool that deliberately tests and selects unfiltered responses; both scanners detect that offensive tool. An ordinary Git installer and unrelated Telegram test fixtures had also produced misleading hostile findings. The installer finding is now suspicious, and the Telegram file-upload finding requires its evidence in one file. A host-reporting PoC control remains hostile in both scanners, while a control archive of the unrelated Hermes files is clear of the exfiltration finding. Full validation passed and Hopper confirmed bad.

- `de028b4fd777701977e34bd5cddd34b0cc5b9d58fb6615180576f557e82c1254` — **good** — Cap screen-recording application source. Both artifact-only scans found no suspicious or hostile findings. Full validation passed and Hopper confirmed good.

- `6fb7df3267702602c437a925475851f3a9b5f98689aa30aec87e2392a2326288` and `7f5ee8a11dfe639165f5430398d924e07652dd86890e94402dd7cec28549d478` — **good** — Windows Runtime binding source archives. Both scanners found no hostile content after correcting findings that treated managed metadata API declarations as executable behavior and Cargo feature declarations as a loader. Full validation passed and Hopper moved both to good.

- `47d6bd56d3a99dab40cdc76271694aed474bfa4a25d4ae8def57b69da54842e9` — **good** — Source for an authorship-evidence utility. Both scanners found no hostile content and one suspicious dependency-combination profile; Atom's artifact-only scan used `--follow none` after the dependency-following run encountered registry rate limits. Full validation passed and Hopper moved it to good.
- `3fa636ea71503610260a3251ee4b34fba76bac4a88d956d6a171e58c73c03542` — **good** — pnpm source includes an intentionally malformed ZIP as inert test data. Both artifact scans found no hostile content; an erroneous Node execution finding on prose about a `.bin` directory was corrected, while a real data-file execution control still matched. Full validation passed and Hopper confirmed good.

The standalone manifests below declare names, dependencies, features, and build settings, but do not contain the referenced program implementations. They were reviewed individually as supporting files, not classified from their parent-project names. Both scanners had no hostile findings after the trait changes; the Phoenix manifest retains one suspicious credential-store dependency profile. The ransomware-themed manifest also retains a suspicious declaration of a ransom-note binary. Full validation passed and Hopper moved each to good.

- `04b2b24852408a6e41a0215ec01afaf39a587eaa492ab3f5165a089da38d2323` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `eb48cf93c26129c6e8cb37fc8a550b22fe3785abb03b6c8d650b22ec231404c3` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `59b844d92ffeae25a44cbeaf09131ef02eb699944c88f8545fcf5970cc99d4d2` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `341b2c130c163dd923e6d4f26c7879268d644342d57b81a18b981327d887121e` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `8f270346194ec9fc0325a00f80b11903f4a12c7eec769bb92d79263e141b454d` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `909951dc262f4e3040e052bada8a84f5ffafe79b64df55102d01a48f7994d083` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `2bee4cc8628c51c2f4465e75bf9f8e0787f67b69881112b66d91f275cc288c8a` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `5a7d0ca8173ba0553d891d6b9fb1fd8fd7a8337eeeb1892550c4941bfabb4443` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `f18d6607a0ef3465f22159e7892ee6123601806ff8d5b12b327ba78a0757a5dd` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `17989b6737f1c785c168d561a4be71e2e20a462fa8e982c1961223cccd4a6b5f` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `148e39669b4e28a5b38750bfa3f5f8dde6a53a29087e44d914e79d79dc806dd0` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `3c64b75140a13102bbbc412b009b3ca716336e74929a1cfba766c7d579cf1e58` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `2921d498f442570ebc491f59e32577b1bf4989c164fbfdf53be00ea5f12b8c36` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `0ffab351bcba26c9d42afbaafffd4a55fc63bd0f2e3d076f67ac813f44f3bdfc` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `1c28c213f40bade3f9330739b4901e4c43b98b8efa3ca83ff0210d3c4ce803ce` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.
- `f9b0d5f2318a13013bf15221d9a117c4b9e6e6b8afcd63319ecfee73b12fde75` — **good** — Standalone Cargo manifest; declared package and dependency metadata only.

- `34f01d6df4b38b123d79e09ac956725a98584aea20e70f14d579cfefd025a091` and `dddb0873e9b2ebf42143c379b12074e505c583107be5b8d772b31959aa5179c5` — **bad** — Dependency-confusion PoC crates whose build scripts gather host/user information and send it to Telegram. Both scanners report hostile build-hook findings. Full validation passed and Hopper confirmed bad.
- `bcd8e4f9fe34af7057a9485badcd302454b45d76d898ae026e3bdabf4af04dfa` — **bad** — The password-protected archive contains a credential-stealing Rust implementation that reads Chromium login databases, decrypts passwords, and writes the results; another source module sends documents through Telegram. Both scanners now match the new Chromium extraction finding on the original archive and source; an altered password-output control clears it in Atom. Full validation passed and Hopper confirmed bad.
