"""Adversarial vectors for an invisible-unicode sanitizer: the smuggled inputs
a defense must flatten, enumerated so the test suite can prove they do."""

import pytest

SMUGGLED_TAG_MESSAGE = "".join(chr(0xE0000 + ord(char)) for char in "ABC")
INVISIBLE_CODEPOINTS = [chr(0xE0000), chr(0xE0041), chr(0xE007F), chr(0xE0100)]


def sanitize(text):
    raise NotImplementedError


def test_smuggled_message_flattens_away():
    assert sanitize(SMUGGLED_TAG_MESSAGE) == ""


@pytest.mark.parametrize("char", INVISIBLE_CODEPOINTS)
def test_every_invisible_character_flattens(char):
    assert sanitize(char) == " "
