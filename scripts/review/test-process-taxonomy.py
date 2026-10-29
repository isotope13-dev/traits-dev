#!/usr/bin/env python3
"""Regression checks for the process boundary, without loading the catalog."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "process_taxonomy", Path(__file__).with_name("check-process-taxonomy.py")
)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ProcessTaxonomyTest(unittest.TestCase):
    def test_every_retired_subtree_rejects_nested_rules(self):
        policy = json.loads(checker.POLICY.read_text())
        for retired in policy:
            with self.subTest(retired=retired), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                nested = root / retired / "new-name" / "rules.yaml"
                nested.parent.mkdir(parents=True)
                nested.write_text("traits: []\n")
                errors = list(checker.violations(root, policy))
                self.assertEqual(len(errors), 1)
                self.assertIn(retired, errors[0])
                self.assertIn("1 YAML files", errors[0])

    def test_valid_resources_and_similar_names_are_not_banned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in (
                "micro-behaviors/process/stdio/relay",
                "micro-behaviors/process/create/fork",
                "micro-behaviors/process/hook/interception",
                "micro-behaviors/process/interpreter/eval/direct",
                "micro-behaviors/data/stream/read",
                "micro-behaviors/communications/http/intercept",
                "micro-behaviors/os/application/hook/event",
            ):
                (root / path).mkdir(parents=True)
            self.assertEqual(list(checker.violations(root, json.loads(checker.POLICY.read_text()))), [])


if __name__ == "__main__":
    unittest.main()
