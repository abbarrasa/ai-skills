"""Exercise packaging failures that would prevent sharing the catalog."""

import tempfile
import json
import unittest
from pathlib import Path

from scripts.validate_skills import validate_catalog


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "skills").mkdir()
        (self.root / "README.md").write_text("# Catalog\n", encoding="utf-8")
        self.graph = {}

    def skill(self, name, content=None):
        folder = self.root / "skills" / name
        folder.mkdir()
        self.graph[name] = ["sdd"] if name.startswith("sdd-") else []
        (self.root / "skills-dependencies.json").write_text(json.dumps(self.graph), encoding="utf-8")
        (folder / "SKILL.md").write_text(
            content if content is not None else
            f"---\nname: {name}\ndescription: Guide creation, review, and validation (SDD).\n---\n\n# Instructions\n",
            encoding="utf-8",
        )

    def test_valid_companion_pack(self):
        self.skill("sdd")
        self.skill("sdd-status")
        self.assertEqual(validate_catalog(self.root), ([], 2))

    def test_missing_companion_is_rejected(self):
        self.skill("sdd-change")
        errors, _ = validate_catalog(self.root)
        self.assertTrue(any("missing dependency" in error for error in errors))

    def test_malformed_or_unsupported_frontmatter_is_rejected(self):
        for content in (
            "# Missing metadata\n",
            "---\nname: example\ndescription: true\n---\nInstructions\n",
            "---\nname: example\nname: example\ndescription: Guide work.\n---\nInstructions\n",
            "---\nname: example\ndescription: |\n  Multiline\n---\nInstructions\n",
            "---\nname: other\ndescription: Guide work.\n---\nInstructions\n",
        ):
            with self.subTest(content=content):
                source = self.root / "skills" / "example"
                source.mkdir(exist_ok=True)
                (source / "SKILL.md").write_text(content, encoding="utf-8")
                self.assertTrue(validate_catalog(self.root)[0])

    def test_missing_entrypoint_and_broken_readme_link_are_rejected(self):
        (self.root / "skills" / "empty").mkdir()
        (self.root / "README.md").write_text("[Missing](skills/missing/SKILL.md)\n", encoding="utf-8")
        errors, _ = validate_catalog(self.root)
        self.assertTrue(any("missing SKILL.md" in error for error in errors))
        self.assertTrue(any("missing linked skill" in error for error in errors))

    def test_empty_catalog_is_rejected(self):
        self.assertTrue(validate_catalog(self.root)[0])


if __name__ == "__main__":
    unittest.main()
