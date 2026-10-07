Alternate path separator traversal controls

ordinary-resource.py and quoted-comment.py must not fire traversal objectives.
encoded-traversal.py is a benign reserved-domain fixture: retain its suspicious
traversal syntax but do not infer hostile file access against example.test.
public-target.py must fire suspicious double-colon-traversal-request.
A target path alone must not establish hostile credential extraction.
mixed-targets.py must also fire traversal, alongside a reserved-domain request.
These fixtures test resource-name independence, URL-encoded dots/colons,
exclusion of prose-only evidence, and request-local target filtering.
