"""Verify transitive installation selections and reject invalid dependency catalogs."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.install_skills import main
from scripts.skill_dependencies import load_dependencies, resolve_dependencies


ROOT = Path(__file__).resolve().parents[1]


class DependenciesTests(unittest.TestCase):
    def test_each_catalog_skill_resolves_its_complete_chain(self):
        graph = load_dependencies(ROOT)
        expected = {
            "feature": ["feature"],
            "sdd-code-review": ["sdd-code-review"],
            "sdd": ["feature", "sdd-code-review", "sdd"],
            "constitution": ["feature", "sdd-code-review", "sdd", "constitution"],
            "sdd-change": ["feature", "sdd-code-review", "sdd", "sdd-change"],
            "sdd-status": ["feature", "sdd-code-review", "sdd", "sdd-status"],
        }
        self.assertEqual(set(graph), set(expected))
        for name, selection in expected.items():
            with self.subTest(skill=name):
                self.assertEqual(resolve_dependencies(graph, [name]), selection)

    def test_shared_dependencies_are_installed_once(self):
        graph = load_dependencies(ROOT)
        self.assertEqual(resolve_dependencies(graph, ["constitution", "sdd-status", "sdd"]),
                         ["feature", "sdd-code-review", "sdd", "constitution", "sdd-status"])

    def test_unknown_skills_missing_dependencies_and_cycles_fail(self):
        for graph, requested in (({"a": []}, ["unknown"]),
                                 ({"a": ["missing"]}, ["a"]),
                                 ({"a": ["b"], "b": ["a"]}, ["a"])):
            with self.subTest(graph=graph):
                with self.assertRaises(ValueError):
                    resolve_dependencies(graph, requested)

    def test_manifest_must_cover_all_catalog_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "skills-dependencies.json").write_text(json.dumps({"missing": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Manifest/catalog mismatch"):
                load_dependencies(root)

    def test_dry_run_never_starts_installer(self):
        with tempfile.TemporaryDirectory() as directory, patch("scripts.install_skills.subprocess.run") as run:
            self.assertEqual(main(["--skill", "sdd-status", "--project", directory, "--dry-run"]), 0)
            run.assert_not_called()

    def test_installer_passes_resolved_selection_and_propagates_failure(self):
        with tempfile.TemporaryDirectory(prefix="project with spaces ") as directory:
            with patch("scripts.install_skills.shutil.which", return_value="/tools/npx"), \
                 patch("scripts.install_skills.subprocess.run") as run:
                run.return_value.returncode = 7
                self.assertEqual(main(["--skill", "sdd-status", "--project", directory, "--yes"]), 7)
                command = run.call_args.args[0]
                self.assertEqual(command[command.index("--skill") + 1:command.index("--agent")],
                                 ["feature", "sdd-code-review", "sdd", "sdd-status"])
                self.assertEqual(run.call_args.kwargs["cwd"], Path(directory).resolve())
                self.assertIn("--copy", command)


if __name__ == "__main__":
    unittest.main()
