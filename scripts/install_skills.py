"""Install selected skills and their dependencies from this exact catalog checkout."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from .skill_dependencies import load_dependencies, resolve_dependencies
except ImportError:
    from skill_dependencies import load_dependencies, resolve_dependencies


def main(argv=None) -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {(root / 'VERSION').read_text(encoding='utf-8').strip()}")
    parser.add_argument("--skill", nargs="+", required=True, help="Skill names, or '*' for the entire catalog")
    parser.add_argument("--project", type=Path, required=True, help="Existing destination project directory")
    parser.add_argument("--agent", nargs="+", default=["codex", "github-copilot"], help="Skills CLI agent names")
    parser.add_argument("--yes", action="store_true", help="Skip Skills CLI confirmation prompts")
    parser.add_argument("--dry-run", action="store_true", help="Print resolved selection and command without installing")
    args = parser.parse_args(argv)
    try:
        graph = load_dependencies(root)
        requested = list(graph) if args.skill == ["*"] else args.skill
        selected = resolve_dependencies(graph, requested)
        project = args.project.resolve()
        if not project.is_dir():
            raise ValueError(f"Destination project does not exist: {project}")
        if project == root or root in project.parents:
            raise ValueError("Choose a destination outside this catalog checkout.")
    except ValueError as exc:
        parser.error(str(exc))
    npx = shutil.which("npx")
    command = [npx or "npx", "--yes", "skills@1.7.6", "add", str(root),
               "--skill", *selected, "--agent", *args.agent, "--copy"]
    if args.yes:
        command.append("--yes")
    print(f"Resolved skills (dependencies first): {', '.join(selected)}", flush=True)
    print(f"Destination: {project}", flush=True)
    print(f"Command arguments: {json.dumps(command)}", flush=True)
    if args.dry_run:
        return 0
    if npx is None:
        parser.error("npx not found. Install Node.js/npm first; this script does not install runtimes.")
    # No shell expansion; all skills come from the same checkout/release.
    try:
        return subprocess.run(command, cwd=project, check=False).returncode
    except OSError as exc:
        print(f"Installation could not start: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
