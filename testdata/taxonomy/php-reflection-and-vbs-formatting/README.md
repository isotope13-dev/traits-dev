# Request reflection and ASP port-reporting review

Sample `f0cdafd36bc702f7ffc6d3a00a231779d8ecbc4a2a848943a5f78cd79c3787bf`
(`Readme.md`): **MALICIOUS**, PHP reflection webshell source presented as a
README example. `$_GET[m]` is passed directly to `ReflectionFunction`; the
result is assigned to `$func`. The immediately following statement calls
`$func->invokeArgs(array($_GET[c]))` and echoes its result. There is no
authentication, function allowlist, argument validation, or other code in this
281-byte artifact. Under PHP 5/7, selecting `system` supplies an OS command;
selecting `file_get_contents` can return a server-readable file. These are
alternative uses of one arbitrary-call capability, not separate observed
payloads. No particular command or file target is embedded.

The Markdown filename does not execute PHP by itself. This verdict identifies
the embedded operational backdoor source, not evidence that a server deployed
or executed it. PHP 8 rejects the unquoted `m`/`c` constants unless separately
defined; the historical bare-key fallback makes this source usable on PHP 5/7.
The relative image reference `11.jpg` has no origin URL and its target is absent
from the supplied sample directory. It contributes no execution behavior.

The new rules require adjacent constructor/dispatch statements with equal
receiver variables. They record request-selected invocation and the stronger
request-selected-function-and-argument case separately. Both remain suspicious:
their general patterns cannot establish whether surrounding application code
authorizes the dispatcher. The complete supplied sample has no such context.
No second hostile outcome is invented to meet a detection count.

Sample `cba58c137c13b07859be5db1095d83794598862d5029a117c1e8361bea5d87ca`
(`ASP读终端端口.ccc`): **BENIGN**, UTF-16LE classic ASP/VBScript port-reporting
fragment. Full BOM decoding reveals thirteen straight-line statements with
three conditional assignments. `Server.CreateObject("WScript.Shell")` creates
an automation object. Its only called method is `RegRead`, applied to the local
Telnet port, Terminal Server transport port, and pcAnywhere data-port values.
The values flow to `Response.Write` as HTML list items. There are no request
inputs, registry writes, process launches, credentials, network clients,
downloads, persistence, or further dependencies/URLs to fetch.

The fallback for Telnet mistakenly assigns `Tlnt` instead of `TlntPort`; the
other outputs also append `TlntPort`. Missing-key errors are not caught, so an
absent key can stop the fragment before its fallback. The standalone file lacks
ASP delimiters and needs an ASP context to run. Neither these bugs nor the
unregistered suffix add hostile behavior. Its external malware label may come
from collection alongside a webshell reconnaissance toolkit; the supplied
fragment does not prove that provenance or unauthorized use.

All ten `Chr` calls in the ASP sample produce CR or LF. The dense-construction
rule now counts complete expressions and removes individual tab/CR/LF/space
calls before applying its threshold. Ten content-building calls still match,
including when formatting calls coexist. Existing localized Unicode exclusion
is preserved. Three notable registry-path observations describe references,
not service activation or registry modification.

`cases.json` records thirteen positive and negative controls. Run
`python3 testdata/taxonomy/php-reflection-and-vbs-formatting/check.py` to verify
them against Cleave's emitted JSON. The original samples were also checked
with `cleave facts`, `cleave test-rules`, and `atomscan`.

Semantic references:

- [ReflectionFunction constructor](https://www.php.net/manual/en/reflectionfunction.construct.php)
- [ReflectionFunction::invokeArgs](https://www.php.net/manual/en/reflectionfunction.invokeargs.php)
- [PHP array keys and historical bare-key fallback](https://www.php.net/manual/en/language.types.array.php)
- [Microsoft registry reads using WScript.Shell](https://learn.microsoft.com/en-us/powershell/scripting/samples/working-with-registry-entries)
