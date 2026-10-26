"""Opt-in product analytics through Segment (opt-out at runtime)."""
import analytics

SEGMENT_WRITE_KEY = "sFM7q98HtHTMmCW3d6nsPWYCIdrbs7gq"


def track_signup(user_id, session_id):
    analytics.write_key = SEGMENT_WRITE_KEY
    analytics.track(
        user_id=user_id,
        anonymous_id=session_id,
        event="Signed Up",
        properties={"plan": "free"},
    )
