# Release comparison controls

Both supplied artifacts are benign. Registry downloads reproduce their supplied
SHA-256 hashes exactly; no specimen code was executed.

* win32-taskscheduler 2.0.0 versus RubyGems 1.0.12:
  https://rubygems.org/downloads/win32-taskscheduler-1.0.12.gem
  The functional spec is byte-identical after correcting its filename from
  taskschedular_spec.rb to taskscheduler_spec.rb. `stop_the_app` executes
  tasklist and conditional taskkill to close iexplore.exe after run/terminate
  tests. Runtime changes move helper namespaces under Win32::TaskScheduler;
  they do not introduce a dropper, encryption, ransom note or exfiltration.
* ART 6.1 versus PyPI 6.0:
  https://pypi.org/pypi/art/6.0/json
  The banner3d ampersand and jazmine w glyphs containing repeated dots/colons
  are unchanged. text_dic1.py changes only blank-space glyph rendering for
  block and danc4 fonts. Other changes improve spacing, Unicode warnings,
  type checks and iteration; get_font_dic/text2art consume the dictionaries
  as character artwork, never filesystem paths.

The current false-positive patterns also exist in the preceding releases.
The release diff therefore does not support compromise or new traversal.

Controls retain actual Ruby execution and encoded traversal, while rejecting
printed/commented commands, glyph shading, suffix concatenation, and XOR
characters within a string. Neutral observations have their capability or
metadata homes; objective composites retain references to the moved facts.
