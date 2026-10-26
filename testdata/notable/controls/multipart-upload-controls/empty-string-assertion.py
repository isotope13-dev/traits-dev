# Regression guard: a unittest asserting on an empty-string record field with
# a doku.php documentation URL nearby is not a multipart upload. The
# client-bypass composite must see a `files` container, not just ("", ...)
# and a .php URL within 200 bytes.
import unittest


class TestParseTestRecord(unittest.TestCase):
    def test_only_strict(self):
        record = {
            "onlyStrict": "",
            "bestPractice": "http://wiki.ecmascript.org/doku.php?id=conventions:no_non_standard_strict_decls",
        }
        self.assertEqual("", record['onlyStrict'])
        self.assertEqual(
            "http://wiki.ecmascript.org/doku.php?id=conventions:no_non_standard_strict_decls",
            record['bestPractice'])
