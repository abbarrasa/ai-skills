# AI Skills

Set of AI skills to manage software projects using the Spec-Driven Development (SDD) methodology.

Current catalog version: **1.0.1**, recorded in [VERSION](VERSION).
Check a local checkout with `python3 scripts/install_skills.py --version`.

## What is Spec-Driven Development?

Spec-Driven Development (SDD) is a software engineering methodology where a clear, structured and readable specification (usually in Markdown files within the project) acts as the source of truth before writing code.
Instead of starting to program directly or giving loose, improvised orders to an artificial intelligence (a phenomenon known as vibe coding), the process is reversed: the code is the consequence of the specification, not the starting point.

### How the workflow works

Although there are variants, the basic cycle in SDD is divided into several phases:

1. Specify: You define precisely what you want to build, the objectives, business rules, limit cases and acceptance criteria.
2. Plan: You translate that intention into a technical architecture and system design (plan.md).
3. Decompose (Tasks): You divide the plan into atomic tasks or small, sequential steps (tasks.md).
4. Implement and verify each task: The agent implements the authorized work and runs the agreed checks for that task.
5. Validate the feature: Review the completed change against the approved specification, trace each requirement to code and verification evidence, and obtain user acceptance before marking the specification implemented.

### Why has Artificial Intelligence gained so much relevance?

With the advent of advanced programming assistants, the bottleneck is no longer typing fast code, but maintaining context control.

- Avoid context drift: When an AI is given vague prompts, it tends to invent logic, break files it doesn't see, or introduce regressions.
- Limit uncertainty: By defining clear boundaries in Markdown, AI stops guessing about the architecture and works on an explicit technical contract.
- Traceability: If months later you wonder why the system makes a specific decision, the answer lives in the versioned specification in Git and not buried in a giant diff.

## Install in any software project

The skills are language-independent Markdown instructions. Keep C#, PHP, or other
stack-specific commands and conventions in each consuming project's instructions
and constitution. Installing these skills does not install application dependencies.

### Install one skill with its dependencies (recommended)

Requirements on the installing machine:

| Tool | Required version | Tested version |
| --- | --- | --- |
| Node.js | 22.20.0 or newer; use the 24.x line to match our tested major version | 24.22.1 |
| npm | Use the version bundled with your Node.js installation | 11.9.0 |
| npx | Included with npm; must be available on `PATH` | Bundled with npm 11.19.1 |
| Python | 3.11 or newer | 3.12.14 |
| Git | Required to clone and select catalog revisions | No specific version pinned |

Node.js 20.x and versions earlier than 22.20.0 do not meet the documented
requirement. The minimum is not a claim that every newer release was tested;
the tested versions above identify the actual installation smoke-test environment.
There is no separate npm or npx installation/version pin for this catalog.
See [Skills CLI prerequisites](https://github.com/vercel-labs/skills#install-a-skill).

Verify availability in the same terminal where you will run the installer:

```bash
node --version
npm --version
npx --version
python3 --version
git --version
```

If `npx` is missing, install Node.js with npm and reopen your terminal before
retrying. None of these tools is added to your application's runtime dependencies.
On Windows, use `python` or `py -3` instead of `python3` if appropriate for your
installation.

Clone this catalog outside the destination project, then run its installer:

```bash
git clone https://github.com/abbarrasa/ai-skills.git
python3 ai-skills/scripts/install_skills.py --skill sdd-status --project /path/to/your-project --dry-run
python3 ai-skills/scripts/install_skills.py --skill sdd-status --project /path/to/your-project
```

The second command previews `feature`, `sdd`, and `sdd-status`. The third installs
that selection using [Skills CLI](https://github.com/vercel-labs/skills) 1.7.6.
The script invokes `npx --yes skills@1.7.6`, which can download that pinned CLI
from npm on first use. It does not install Python, Node.js, or npm for you.
By default it targets Codex and GitHub Copilot. Override with `--agent codex`,
for example; pass `--yes` only when you want to skip installer confirmations.
The destination directory must already exist and be outside the catalog checkout.

Select multiple skills or the entire catalog:

```bash
python3 ai-skills/scripts/install_skills.py --skill constitution sdd-change --project /path/to/your-project --agent codex
python3 ai-skills/scripts/install_skills.py --skill '*' --project /path/to/your-project
```

To install code review and its complete dependency chain (`feature`, `sdd`,
`sdd-code-review`), run:

```bash
python3 ai-skills/scripts/install_skills.py --skill sdd-code-review --project /path/to/your-project
```

Dependencies are declared once in [skills-dependencies.json](skills-dependencies.json).
The installer resolves transitive dependencies, installs each once, and checks
for unknown skills, missing catalog entries, and cycles before invoking Skills CLI.
All files come from the same local checkout, including uncommitted changes: use
a clean checkout of a reviewed release for established projects.

The installer uses copies, not symlinks. For Codex and GitHub Copilot,
the installer currently targets `.agents/skills/`. Other agents may use different
locations; let the installer choose them. See its
[agent compatibility table](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).

Commit the installed skill folders and any installer-generated lockfile to the
destination project's Git repository. Review the diff before committing; do not
overwrite locally customized skills without reconciling their changes.

For a reproducible installation, check out a published tag or full commit SHA
before running the script. **This example requires a published `v1.0.1` tag:**

```bash
git -C ai-skills checkout v1.0.1
python3 ai-skills/scripts/install_skills.py --skill sdd-status --project /path/to/your-project
```

Record the catalog's Git commit/tag alongside the installed files. Skills CLI's
lockfile may identify the source as a local checkout path, which is not a portable
replacement for recording the Git revision. Keep the clone for future updates;
the installed copies do not depend on it at runtime. See the official
[command reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

The six-skill catalog was smoke-tested with the versions above and Skills CLI
1.7.6. The smoke test verified discovery and byte-for-byte copies for Codex,
GitHub Copilot, and Claude Code.

To test unpublished changes, run the same script from your local catalog checkout
with an existing disposable destination directory.

### Direct Skills CLI installation

Skills CLI does not resolve this catalog's dependency manifest. If you bypass
our script, explicitly include every dependency or install the entire catalog.
From the destination project, the complete set can be installed with:

```bash
npx skills@1.7.6 add abbarrasa/ai-skills --skill feature sdd-code-review sdd constitution sdd-change sdd-status --agent codex github-copilot --copy
npx skills@1.7.6 list
```

## Available skills

| Skill | Purpose | Required companions |
| --- | --- | --- |
| [sdd](skills/sdd/SKILL.md) | Complete SDD workflow and approval gates | `feature` |
| [constitution](skills/constitution/SKILL.md) | Propose and approve project principles | `sdd` |
| [sdd-change](skills/sdd-change/SKILL.md) | Change requirements before downstream implementation | `sdd` |
| [sdd-status](skills/sdd-status/SKILL.md) | Read-only phase, progress, and next-step report | `sdd` |
| [sdd-code-review](skills/sdd-code-review/SKILL.md) | Read-only code review against an approved spec and change scope | `sdd` |
| [feature](skills/feature/SKILL.md) | General feature planning before implementation | None |

The table lists direct dependencies. The wrapper installs dependencies transitively
in the destination project. SDD phase approvals still apply. Use direct Skills CLI
with `--global` for intentional personal installations and include the complete
dependency selection.

`sdd-code-review` extends `sdd`; the base workflow does not install the review
extension. Install it before completing SDD validation. Installing `sdd-status`,
`sdd-change`, or `constitution` alone brings in `sdd` and `feature` only.

## Use in a destination project

1. Verify that your agent discovers the installed skills. Invoke them explicitly
   when needed; for Codex, for example: `$constitution`, `$sdd`, or
   `$sdd-status specs/001-feature-name/`.
2. Record the project's actual build, test, and quality commands in its repository
   instructions. Keep technology choices and approved principles in its
   `docs/constitution.md`, feature documents in `specs/`, and progress in `MEMORY.md`.
3. Keep shared skills unchanged where possible. Put local conventions in project
   instructions and propose reusable workflow improvements in this catalog.

### Review a completed implementation

After authorizing validation, identify the feature directory and the change scope
to review. In Codex you can run the review separately, preferably in a fresh
session. Replace the example path and target branch with your project's values.

```text
$sdd-code-review specs/001-feature-name/ Review committed HEAD changes for a merge into dev.
```

You can also provide a PR reference and let the reviewer resolve its actual base
and head. For agents without skill discovery, give the agent the installed
`sdd-code-review/SKILL.md` path and the same inputs.

Use the review report in `sdd` validation. **PASS** supplies review evidence for
the user's acceptance of validation. **CHANGES REQUESTED** identifies blockers
for authorized corrective work. **INCOMPLETE** identifies missing scope or
verification evidence. Recheck the updated scope after fixes.

## Updates and releases

Use a deliberate upgrade PR in each consuming project. Update the catalog clone
to the chosen newer tag or full commit and re-run the dependency-aware installer
for the desired skills. Review all installed changes, verify agent
discovery, and record the source revision and installer version. Avoid automatic
upgrades from a moving branch for established projects.

This catalog uses `vMAJOR.MINOR.PATCH` tags: major for incompatible workflow,
approval, or document-contract changes; minor for compatible capabilities or new
skills; patch for corrections that preserve those contracts. Do not move a
published tag. Version 1.0.1 adds the code-review extension and corrects its
installation dependency to `sdd` (which depends on `feature`). Update [VERSION](VERSION)
and the release examples together when preparing a release. Remove local skill
overrides only after reviewing their purpose.

Before publishing a release:

1. Run the local checks below and require the **Validate skills** workflow to pass.
2. Smoke-test installation and agent discovery in a disposable destination project,
   then exercise representative C# and PHP workflows without embedding their stack
   assumptions in the shared skills.
3. Review changes since the previous tag, choose the version, and publish a GitHub
   release and tag for the reviewed commit. Publishing remains a separate action;
   this repository's validation workflow does not publish releases.

## Contributing and validation

Each distributable skill lives at `skills/<name>/SKILL.md`. To keep this small
catalog dependency-free, its frontmatter convention is exactly two single-line,
plain YAML strings: `name` and `description`. Quote-free text must satisfy the
validator's conservative YAML checks; do not use multiline or nested metadata
without first extending validation with a YAML parser.

### Python environment

Python 3.11 or later is required for the dependency-aware installer and catalog
checks. For development, use Python 3.13 to match the major/minor version used by
GitHub Actions. CI currently selects the 3.13 line rather than an exact patch
version; this does not guarantee an identical interpreter across machines.
If the project adopts an exact development version, record it in a committed
`.python-version` file and keep CI aligned with it.

The scripts and tests use only Python's standard library, including `unittest`.
No Python package installation is required, so the catalog currently has no
`requirements.txt`. A virtual environment is optional, but can help keep your
development environment isolated.

From the catalog checkout, with Python 3.13 already installed, create and activate
a virtual environment on Linux or macOS:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, use:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Keep `.venv/` out of version control. Recreate the environment locally instead
of sharing or committing it. Run `deactivate` when finished.

Node.js, npm, npx, and Skills CLI are separate prerequisites for installing skills;
a Python virtual environment does not provide them. See the installation
requirements above.

If third-party Python packages are introduced, declare the project's actual
dependencies in `requirements.txt` or `pyproject.toml`. For reproducible package
versions, pin direct and transitive dependencies or commit an appropriate lockfile.
Avoid generating a requirements file from a personal environment with unrelated
packages.

### Run the checks

With the virtual environment activated, run:

```bash
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

Without a virtual environment, use `python3` on Linux/macOS or `py -3.13` on
Windows in place of `python`, selecting a supported interpreter.

The checks validate catalog packaging, naming, descriptions, dependency graph integrity,
and referenced catalog links. They do not prove agent behavior or SDD compliance.
GitHub Actions runs the same checks on pull requests, pushes, and manual dispatch.

## License

See [LICENSE](LICENSE) for this repository's license. Preserve the license and
applicable notices when redistributing copies of these materials.
