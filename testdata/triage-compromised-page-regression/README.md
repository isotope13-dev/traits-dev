# Compromised-page triage regression

Fixtures for triaging two VirusShare HTML pages (October 2026):

- `repeated-script-inject.html` models the Hebrew WordPress page carrying
  ~250 mass-repeated remote loader tags across rotating hosts (verified
  live: a redirector gateway plus a page-URL-exfiltrating script
  injector). Must fire the massed-tags atom and both injection
  composites.
- `many-scripts-benign.html` is an ordinary six-library page. None of the
  new traits may fire.
- `atob-eval-loader.html` models the Portuguese page's three-stage loader
  (`var X = atob('<1.2KB blob>'); eval(X)`, concealing subtractive
  fromCharCode, XOR and `new Function` layers plus a cloaked conditional
  redirect). Must fire both atob-eval composites.
- `atob-data-benign.html` decodes a small config string with no eval.
  None of the new traits may fire.
- `prize-scam-funnel.html` models the fake-bank survey kit
  ("Congratulations! ... 5000 Dollar", "Share with 5 groups/20
  friends", `whatsapp://send` launcher). Must fire the congratulations
  claim and funnel.
- `legit-congrats-benign.html` is a graduation page (congratulations,
  uncapped share, no cash, no deep link). None of the funnel traits may
  fire.

Run: `python3 testdata/triage-compromised-page-regression/check.py
[--cleave-output.json]`. Fixtures are scanned as copies outside the repo
because some legs carry test-directory exclusions on fixture paths.
