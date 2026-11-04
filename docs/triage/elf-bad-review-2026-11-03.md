# ELF mislabeled-bad review — 2026-11-03

The snapshot contains 40 artifacts, including ELF files and archives that contain ELF files. Both scanners are run with caching disabled; inspection does not execute samples.

`71cb1a76bc1a` remains bad: disassembly shows ten threads repeatedly sending raw TCP SYN packets to a chosen target for a supplied duration. The new `native-threaded-syn-packet-flood` combines the sending function, SYN error message, target/duration usage, and thread evidence. Both scanners report it as hostile; altering the SYN message clears the finding.

`1943b5acf1ee` remains bad: its POP3 source includes a hidden pre-authentication command that invokes an interactive shell. The earlier `sentinel-conjunct-in-auth-predicate` finding was a false positive caused by a single account-lock check matching both comparison atoms. That rule now requires the comparisons to share an AND predicate; the account check clears and a representative magic-password condition still matches. The new `pop3-hidden-command-interactive-shell` detects the actual backdoor in both scanners, and replacing the shell command clears it.

`342b3a213e9b` is good: its entire main function prints its process ID and sleeps repeatedly; its message calling itself a bot does not establish hostile functionality. `286708a5ddd7` and `7f0780cd5ef7` are good: they are standalone ring cryptographic arithmetic object files, with no attack implementation. `99ede26877e2` is the Android SDK zip alignment utility and is good on its own.

Full validation passed after these changes. A slow JavaScript tree query was narrowed to declaration nodes while retaining its existing validation coverage.

`7f13dfe9753e`, `2918231181dd`, `588ef3387aba`, `0e5aeafcf6aa`, and `5889b38cf051` were moved to good: inspection identifies them respectively as a util-linux unmount utility, two GNU timeout builds, a ping utility, and a SQLite interop library. Their collection context does not make these standalone components malicious.

`603540b78ad6` remains bad: its Java archive includes a Fabric initializer that collects Minecraft account and access-token fields for an HTTP request, and the existing scanner findings identify that exfiltration and related staging. `ad69e198905a` remains bad: Go build metadata and embedded symbols identify a post-exploitation agent with injection, persistence, and command-channel code; both scanners report the existing hostile finding.

`4dccca539ad7` is inconclusive. Its encrypted ZIP was opened using the standard infected-sample password; the package manifest and native module were inspected, and the extracted module was scanned directly without a hostile finding. That does not establish whether the native module was altered maliciously. `92dd67a673bc` is inconclusive: its 7z archive contains a 149 MB ELF identifying itself in Go build metadata as a modified Trivy security scanner; the available inspection cannot establish whether the modifications are malicious.

`f1b7b400684f`, `4fd85348909c`, `04a484f27a4b`, `2c336c63e268`, `1f005f89d541`, and `c0db6e0fefb8` were moved to good after inspection identified an Intel SGX runtime library, an Android React Native library, two GNU Bash builds, Android's LLD linker, and an unmodified Lima guest-agent build, respectively. No hostile finding was present in either scanner.

`acf93b80ea57` remains bad. Its npm package runs a Bun setup script at preinstall and contains the large obfuscated Shai-Hulud payload; existing findings in both scanners identify its secret-collection and destructive behavior.

`e70e96983734` and `95884b248875` are inconclusive: they respectively contain an SBCL runtime with a bundled image and an Android executable using TensorFlow Lite; inspection did not establish the behavior of the embedded Lisp image or the Android program. `396cef4f2e86` is a dual-use proxy client package: its manifest, installation scripts, UI, and proxy geography data support that role, while the scans did not establish an additional hostile deployment. Hopper places it in the excluded inconclusive pool because it has no separate dual-use target.

`0fe7a6b691fd` was moved to good. It is an IBM i build extension; inspection of its bundled code showed SSH credentials being used in the extension's configured connection flow, and both scanners reported no hostile findings.

`1880109251f4` and `e51dd0564b04` were moved to good. Both are Node/Debian root filesystems containing the standard Node entrypoint and npm installation; both scanners inspected thousands of members without hostile findings.

`aa56f350882c` remains bad: its 15 MB APK declares an 803 MB Android manifest compressed to about 2 MB, an extreme obstruction to inspection and resource abuse. The new `apk-oversized-compressed-manifest-obfuscation` combines the manifest ZIP header and archive expanded-size facts; both scanners report it as hostile, a header-size mutation clears that finding, and full validation passed. The manifest also declares accessibility, SMS, screen-capture, and other sensitive permissions; those permissions alone do not prove how they are used.

`fe0f4e3d2a90` is good: the xz/tar contains a NeuVector security-monitoring agent. Both scanners reported no hostile findings on the archive and extracted executable. Hopper already held it in good, so the requested move was a no-op.

`c0a777e5122b` and `e899791eb4dc` are good: they contain quantitative-analysis and application-platform packages, respectively; their entry points and packaged contents were inspected, and both scanners reported no hostile findings. `7760f2689454` is inconclusive: it presents itself as a cryptocurrency wallet, but the available analysis does not establish whether its implementation is authentic or malicious. `b83e49a0b187` is a dual-use Android proxy client; it is stored in Hopper's excluded inconclusive pool because Hopper has no dual-use target.

`dbe92ed81c1b` and `b4e86a485629` were moved to good: they contain source for an identity service and a screen-recording application. Their source archives were scanned without hostile findings, and inspection of their package contents did not establish malicious behavior.

`f619bac4e679` was moved to good. It is a bundled development CLI; its postinstall copies its packaged terminal UI dependencies, and the scans reported no hostile findings. `4d096a4d27f5` is inconclusive: it is a .NET executable with substantial embedded resources and Python runtime material, but the available inspection did not establish what all the embedded code does.

`a2d8b7b2adc6` is inconclusive. The encrypted archive contains a modified CLI and a 311 MB executable. The package scripts were inspected and the executable was extracted without execution; both scanners reported no hostile findings on that executable, but the native changes could not be fully established.

`758f5d74da9a` is inconclusive. Its Alpine package identifies itself as Vite, and the extracted JavaScript entry points scanned without hostile findings. Full-package scans timed out in both scanners, including a repeated Cleave attempt, so the complete packaged contents could not be assessed.

The 40 artifacts comprise 6 bad, 24 good, 2 dual-use, and 8 inconclusive. The most recent full validation passed after the trait changes.
