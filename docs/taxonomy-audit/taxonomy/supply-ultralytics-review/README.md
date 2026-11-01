# Ultralytics supply-chain review

The known mining wallet now sits under the Ultralytics miner family. Its exact value is a family-specific signature and no longer has an arbitrary upper file-size limit. The runner string is an Ultralytics-specific reference; XMRig and SupportXMR are product and pool references, not unique to this attack.

Generic `safe_run` source references, Linux platform and `os.system` clues, and GitHub blob/execution-related clues moved to profiles. The previous family rollup could match on a generic Linux platform check or XMRig pool string alone. It now requires the known wallet or the Ultralytics runner plus `safe_run` clues; the latter remains suspicious because it does not itself establish mining.
