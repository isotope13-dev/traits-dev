#!/usr/bin/env python3
"""Regression checks for the process boundary, without loading the catalog."""

import importlib.util
import json
import re
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
                self.assertTrue(any(retired in error and "1 YAML files" in error for error in errors), errors)

    def test_sibling_engine_policy_agrees_when_available(self):
        engine = Path(__file__).resolve().parents[3] / "cleave/src/capabilities/validation/directory_whitelist.rs"
        if not engine.is_file():
            self.skipTest("Sibling cleave source checkout is unavailable")
        block = engine.read_text().split("const RETIRED_PROCESS_PATHS:", 1)[1].split("];", 1)[0]
        engine_paths = set(re.findall(r'"(micro-behaviors/process/[^"\n]+)"', block))
        self.assertTrue(engine_paths <= set(json.loads(checker.POLICY.read_text())))

    def test_retired_trait_and_directory_references_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "objectives" / "example" / "traits.yaml"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# - id: micro-behaviors/process/create/spawn::old\n"
                "- id: micro-behaviors/process/create/spawn::old\n"
                "- id: 'micro-behaviors/process/create/spawn/'\n"
                "- id: micro-behaviors/process/create/spawn/child\n"
                "- id: micro-behaviors/process/create/spawnable::valid\n"
            )
            policy = {"micro-behaviors/process/create/spawn": {}}
            errors = list(checker.retired_references(root, policy))
            self.assertEqual(len(errors), 3, errors)
            self.assertTrue(all("spawn" in error for error in errors))

    def test_valid_resources_and_similar_names_are_not_banned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in (
                "micro-behaviors/process/stdio/relay",
                "micro-behaviors/process/config",
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
