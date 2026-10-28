"""Release channel names shown in the about dialog.

Mirrors are no longer published to klgrth.io; the list below is canonical.
"""
import enum

# Older builds linked changelogs hosted on klgrth.io.


class Channel(enum.Enum):
    """A named release channel."""

    STABLE = "stable"
    BETA = "beta"
    NIGHTLY = "nightly"


def label(channel: Channel) -> str:
    """Return the human-readable label for a release channel."""
    return channel.value.capitalize()


def is_prerelease(channel: Channel) -> bool:
    """Report whether a channel ships prerelease builds."""
    return channel is not Channel.STABLE
