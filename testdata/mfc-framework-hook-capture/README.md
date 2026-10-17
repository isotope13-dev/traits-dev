# GUI framework libraries are not surveillance tools
====================================================

`persistent-keylogger-desktop-surveillance` combines GDI screen capture,
desktop-window access, hook lifecycle, registry writes and process
termination. GUI frameworks expose that whole surface as ordinary
application plumbing: the Microsoft MFC runtime (`mfc140u.dll`) matches
every leg while doing nothing on its own. The composite therefore excludes
catalogued libraries (`well-known/lib/`); an identical binary without
framework identity still convicts.

Run `python3 testdata/mfc-framework-hook-capture/verify.py
<scratch-directory>`. The plain positive must report the hostile; the
framework-marked fixture must not.
