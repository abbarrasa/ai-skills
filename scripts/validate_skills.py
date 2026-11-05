"""Validate this catalog's intentionally restricted, dependency-free skill format."""

import re
import sys
from pathlib import Path

try:
    from .skill_dependencies import load_dependencies
except ImportError:
    from skill_dependencies import load_dependencies

NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def plain_string(value: str) -> bool:
    """Accept a conservative subset of YAML plain string scalars."""
    return bool(value) and not (
        value[0] in "-?:,[]{}#&*!|>'\"%@`"
        or re.search(r":(?:\s|$)|\s#", value)
        or value.lower() in {"true", "false", "null", "~", "yes", "no", "on", "off"}
        or re.fullmatch(r"[\d.+-]+", value)
    )


def validate_catalog(root: Path) -> tuple[list[str], int]:
    errors = []
    skills_dir = root / "skills"
    directories = sorted(path for path in skills_dir.iterdir() if path.is_dir()) if skills_dir.is_dir() else []
    if not directories:
        return ["No skill directories found under skills/."], 0
    names = set()
    for directory in directories:
        source = directory / "SKILL.md"
        label = source.relative_to(root)
        if not source.is_file():
            errors.append(f"{label}: missing SKILL.md")
            continue
        try:
            content = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{label}: cannot read UTF-8 text: {exc}")
            continue
        match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", content, re.DOTALL)
        if not match:
            errors.append(f"{label}: expected YAML frontmatter followed by a body")
            continue
        fields = {}
        for line in match[1].splitlines():
            field = re.fullmatch(r"(name|description): (.+)", line)
            if not field or not plain_string(field[2]):
                errors.append(f"{label}: use only single-line plain name/description strings")
                continue
            key, value = field.groups()
            if key in fields:
                errors.append(f"{label}: duplicate {key} field")
            fields[key] = value
        if set(fields) != {"name", "description"}:
            errors.append(f"{label}: name and description are required")
        name = fields.get("name", "")
        if not NAME.fullmatch(name) or len(name) > 64 or name != directory.name:
            errors.append(f"{label}: name must match its directory and use lowercase hyphenated words (max 64 characters)")
        if name in names:
            errors.append(f"{label}: duplicate skill name {name!r}")
        names.add(name)
        description = fields.get("description", "")
        if not description.strip() or len(description) > 1024 or any(c in description for c in "<>"):
            errors.append(f"{label}: description must be nonempty, at most 1024 characters, without angle brackets")
        if not match[2].strip():
            errors.append(f"{label}: empty instruction body")
    try:
        load_dependencies(root)
    except ValueError as exc:
        errors.append(str(exc))
    readme = root / "README.md"
    if not readme.is_file():
        errors.append("README.md is missing")
    else:
        for target in re.findall(r"\]\((skills/[^)]+)\)", readme.read_text(encoding="utf-8")):
            if not (root / target).is_file():
                errors.append(f"README.md: missing linked skill file {target}")
    return errors, len(directories)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors, count = validate_catalog(root)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"Validated {count} skills: catalog checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
