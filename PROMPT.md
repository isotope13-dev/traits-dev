Improve cleave's detection for this malware sample by editing the YAML files in this directory.

**File**: /data/samples/bad/datasets/vxunderground-inthewild/InTheWild.0288/2026-02-09_ae72bff904c11dcc689ce65a479c8020_amadey_elex_redline-stealer_smoke-loader_stealc_stop
**SHA256**: 5acf169e2b184a3b1454db7883210a9e62704edc9a8da5a34f1cc6fd4288b42f
**Reverse-engineering report**: /var/lib/cyclotron/data/cyclotron/reports/5acf169e2b184a3b1454db7883210a9e62704edc9a8da5a34f1cc6fd4288b42f.md

First, read the reverse-engineering report at /var/lib/cyclotron/data/cyclotron/reports/5acf169e2b184a3b1454db7883210a9e62704edc9a8da5a34f1cc6fd4288b42f.md.
Then perform a reverse-engineering gap analysis: compare `cleave /data/samples/bad/datasets/vxunderground-inthewild/InTheWild.0288/2026-02-09_ae72bff904c11dcc689ce65a479c8020_amadey_elex_redline-stealer_smoke-loader_stealc_stop` against that reverse-engineering report.
Save the reverse-engineering gap analysis to /var/lib/cyclotron/state/cyclotron/2016e52a/scratch/gaps/5acf169e2b184a3b1454db7883210a9e62704edc9a8da5a34f1cc6fd4288b42f.md.

If sample is actually benign: `touch /data/samples/bad/datasets/vxunderground-inthewild/InTheWild.0288/._2026-02-09_ae72bff904c11dcc689ce65a479c8020_amadey_elex_redline-stealer_smoke-loader_stealc_stop.BENIGN` and exit.

### Rules

Improve the traits so that they detect every notable (from a security point of view) characteristic or behavior of this file,
with as few false positives or misleading results as possible:

* To understand the available rules, read all of RULES.md
* If it's create or move a YAML file read TAXONOMY.md for our strict directory layout

- Precision:
  - Write precise rules that only match what they intended to detect.
  - Before adding a pattern, consider what else could contain this string or exhibit this behavior.
  - Prefer `word:` over `substr:`, use `count_min:` for common strings, scope with `for:` to specific file types, and combine low-signal atoms into composites rather than promoting them individually
  - Focus on traits that can detect similar future attacks, not just this past attack.
- Counts:
  - For real malware, aim for 2-4 hostile composite findings, and 3-6 suspicious findings
  - If the sample is from a well-known malware family - aim for at least one hostile finding in the well-known/malware directory - and 1-2 in the objectives/ directory.
- Noteworthiness: findings that would be interesting for differential analysis in a supply-chain attack (networking, execution, privileges) should be `notable` or higher
- Duplication:
  - Search for existing similar rules to improve before adding new ones
- Performance:
  - 'kv' and 'symbol' searches are the fastest and most accurate search types, followed by 'text', then 'hex' and 'raw' (slowest)
  - Keep regexes under 80 chars with at most 4 pipes; splitting them into multiple traits is preferred
- Taxonomy:
  - `objectives/` traits should usually reference `micro-behaviors/` traits rather than duplicate the same low-level pattern
  - Traits detecting neutral capabilities (single API calls, syscalls, common strings, file format markers) belong in `micro-behaviors/` or `metadata/`, NOT `objectives/`. Quick test: would this trait fire on `/bin/ls`? If yes, it is too broad for `objectives/`.

### Useful tools

To reveal characteristics to write rules against: `cleave [strings|symbols|sections|metrics] <file>`

To test your rules:
  cleave test-rules <file> --rules "rule-id"
  cleave test-match <file> --type text --pattern "X"

### Steps1. Create a reverse-engineering gap analysis from cleave's output versus the reverse-engineering report. 
2. Create or improve traits - strictly following TAXONOMY.md
3. Verify detection: `cleave /data/samples/bad/datasets/vxunderground-inthewild/InTheWild.0288/2026-02-09_ae72bff904c11dcc689ce65a479c8020_amadey_elex_redline-stealer_smoke-loader_stealc_stop`
4. Fix any false-positives or misleading results output by cleave (often fixed by relocating a rule or adding constraints to it)
5. Run 'make validate' and fix any warnings or errors displayed by it
