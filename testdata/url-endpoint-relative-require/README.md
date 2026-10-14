URL endpoint tokens versus relative module paths
==================================================

The `group-collection-path-token`, `domain-collection-path-token` and
`organization-path-token` traits match a `/groups`, `/domains` or
`/organization` path segment as evidence of a REST collection URL. Their
matchers used to fire on relative module paths too: every Baileys-family
file with `require("./groups")` reported a "group collection URL path
segment". The regexes now consume one preceding character and require it
not to be a dot, so `./groups` and `../domains` no longer match while
`https://graph.microsoft.com/v1.0/groups` still does.

Run `python3 testdata/url-endpoint-relative-require/check.py
<scratch-directory>`. `graph-collection-url.js` must report all three
tokens; `relative-module-require.js` must report none of them.
