"""Minimized secret-redaction docstring shape: the OAuth bearer body format
quoted to explain a nested field-value judgment. Describing the format is
not posting it, so the OWA bearer-body trait must stay quiet here via the
detection-tool context (this file lives in the agent_sanitizer package).
"""


def _field_value_re(*, nested: bool):
    """The ``field = value`` regex. ``nested`` builds the variant tried INSIDE a
    value already judged benign — a value made of further pairs, joined by a
    pair delimiter (`&` `;` `,`). Its value stops at that delimiter, so
    `token_type=bearer&access_token=X&expires_in=3600` judges `X` on its own
    span and the redaction leaves `&expires_in=3600` in place.
    """
    return nested
