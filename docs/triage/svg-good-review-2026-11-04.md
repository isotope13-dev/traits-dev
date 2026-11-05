# SVG mislabeled-good review, 2026-11-04

Thirty-five small samples parse as XML and have no suspicious or hostile
scanner findings. Static inspection found no script elements, event handlers,
embedded data URIs, or external-resource URLs. Four have `foreignObject`
elements: two contain Illustrator metadata, and two contain empty layout
divs. Their endpoint rulings are good; recording awaits a passing repository
validation while concurrent taxonomy changes settle.

`e4f00ec72fbd` is a VS Code icon-theme extension with no extension
entrypoint, and `172a2f31253c` is a Coinbase Wallet extension. The wallet
requests tab, scripting, storage, and HTTPS host permissions; inspection of
its bundled network destinations found vendor, blockchain RPC, documentation,
and asset endpoints, and the archive scan reported no suspicious or hostile
traits. Both endpoint rulings are good, pending validation and Hopper.

`7e640020b67d` is the GiveWP donation plugin. A preliminary scan covered
3,649 components and reported no suspicious or hostile traits, but it skipped
one malformed rule file from concurrent work. A complete rescan is required
before a verdict.

The remaining two software archives in the pool are still under review; one
preliminary scan also skipped that rule file and must be repeated.
