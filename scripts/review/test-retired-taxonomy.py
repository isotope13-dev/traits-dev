#!/usr/bin/env python3
"""Verify retired taxonomy paths and references cannot be reintroduced."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('retired_taxonomy', Path(__file__).with_name('check-retired-taxonomy.py'))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class RetiredTaxonomyTest(unittest.TestCase):
    def test_rejects_branch_and_live_references_but_not_siblings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            branch = root / 'objectives/credential-access/theft/authentication/keywords'
            branch.mkdir(parents=True)
            (branch / 'rules.yaml').write_text('traits: []\n')
            rules = root / 'metadata/credential/rules.yaml'
            rules.parent.mkdir(parents=True)
            rules.write_text(
                '# - id: objectives/credential-access/theft/authentication::old\n'
                '- id: objectives/credential-access/theft/authentication/keywords::old\n'
                '- id: "objectives/credential-access/theft/authentication/"\n'
                '- id: objectives/credential-access/theft/authentication-helper::valid\n'
                '- id: objectives/credential-access/files/theft::valid\n'
            )
            errors = list(checker.violations(root))
            self.assertEqual(len(errors), 3, errors)


    def test_empty_directory_is_allowed_but_nested_yaml_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            branch = root / 'micro-behaviors/data/db/sql'
            branch.mkdir(parents=True)
            self.assertEqual(list(checker.violations(root)), [])
            child = branch / 'nested'
            child.mkdir()
            (child / 'rules.yml').write_text('traits: []\n')
            errors = list(checker.violations(root))
            self.assertTrue(any('micro-behaviors/data/db/sql:' in error for error in errors), errors)


if __name__ == '__main__':
    unittest.main()
