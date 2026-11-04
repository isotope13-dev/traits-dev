# GYP mislabeled-bad review — 2026-11-03

Both samples are npm package archives rather than standalone GYP files. `72e436ffd5c5` and `f59f262bb51b` remain bad. Each contains an index script that reconstructs a character-code array, shifts its letters, and evaluates a loader that decrypts two AES-GCM blobs. Offline decryption revealed a further heavily obfuscated script and a loader that writes it to a randomly named temporary JavaScript file, runs it with Bun, and removes the file. The loader can also obtain a Bun runtime. The `leo-connector-redshift` package points its main entry at the wrapper; the other package contains the wrapper even though its declared main entry points elsewhere.

Both Cleave and Atom detect the encrypted execution chain. Added a second hostile composite that combines the existing AES-GCM and indirect-evaluation finding with temporary-script creation and Bun execution. It matches both archives in both scanners; a control changing the execution to a build command clears the new composite. No samples were executed, and no scanner engine feature was added.

Full validation passed, and Hopper confirmed both bad labels.
