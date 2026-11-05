# AI Skills

Set of AI skills to manage software projects using the Spec-Driven Development (SDD) methodology.

## What is Spec-Driven Development?

Spec-Driven Development (SDD) is a software engineering methodology where a clear, structured and readable specification (usually in Markdown files within the project) acts as the source of truth before writing code.
Instead of starting to program directly or giving loose, improvised orders to an artificial intelligence (a phenomenon known as vibe coding), the process is reversed: the code is the consequence of the specification, not the starting point.

### How the workflow works

Although there are variants, the basic cycle in SDD is divided into several phases:

1. Specify: You define precisely what you want to build, the objectives, business rules, limit cases and acceptance criteria.
2. Plan: You translate that intention into a technical architecture and system design (plan.md).
3. Decompose (Tasks): You divide the plan into atomic tasks or small, sequential steps (tasks.md).
4. Implement & Verify: You deliver this structured documentation to a code agent (such as Claude Code, GitHub Copilot, or Cursor) to generate code and tests within those strict boundaries, verifying that it meets the original specification.

### Why has Artificial Intelligence gained so much relevance?

With the advent of advanced programming assistants, the bottleneck is no longer typing fast code, but maintaining context control.

- Avoid context drift: When an AI is given vague prompts, it tends to invent logic, break files it doesn't see, or introduce regressions.
- Limit uncertainty: By defining clear boundaries in Markdown, AI stops guessing about the architecture and works on an explicit technical contract.
- Traceability: If months later you wonder why the system makes a specific decision, the answer lives in the versioned specification in Git and not buried in a giant diff.

## Install in any software project

The skills are language-independent Markdown instructions. Keep C#, PHP, or other
stack-specific commands and conventions in each consuming project's instructions
and constitution. Installing these skills does not install application dependencies.

Use [Skills CLI](https://github.com/vercel-labs/skills), with Node.js 22.20 or later
on the installing machine. From the root of the destination project:

```bash
npx skills@1.7.6 add abbarrasa/ai-skills --list
npx skills@1.7.6 add abbarrasa/ai-skills --skill sdd constitution sdd-change sdd-status feature --agent codex github-copilot --copy
```

These commands use the repository's default branch, so only committed and pushed
skills are available. Select only the agents you use. For Codex and GitHub Copilot,
the installer currently targets `.agents/skills/`. Other agents may use different
locations; let the installer choose them. See its
[agent compatibility table](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).

Commit the installed skill folders and any installer-generated lockfile to the
destination project's Git repository. Review the diff before committing; do not
overwrite locally customized skills without reconciling their changes.

For a reproducible installation, replace the default branch with a published tag
or full commit SHA. **The following example requires a published `v1.0.0` tag; it
does not create one:**

```bash
npx skills@1.7.6 add abbarrasa/ai-skills@v1.0.0 --skill sdd constitution sdd-change sdd-status feature --agent codex github-copilot --copy
```

For strict reproducibility, also record and pin the tested Skills CLI version
using `npx skills@<CLI_VERSION>`. The CLI is an installation tool, not a dependency
of the C# or PHP application. See the official
[command reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

The local catalog was smoke-tested with Node.js 24.22.2, npm 11.19.1, and Skills
CLI 1.7.6: all five skills were discovered, installed with `--copy` for Codex and
GitHub Copilot, and compared byte-for-byte with the sources. This verifies
installation, not agent execution or the behavior of a published release.

To test unpublished changes, run this from a disposable destination directory,
replacing the source path with your local checkout:

```bash
npx skills@1.7.6 add /absolute/path/to/ai-skills --skill sdd constitution sdd-change sdd-status feature --agent codex github-copilot --copy
npx skills@1.7.6 list
```

## Available skills

| Skill | Purpose | Required companion |
| --- | --- | --- |
| [sdd](skills/sdd/SKILL.md) | Complete SDD workflow and approval gates | None |
| [constitution](skills/constitution/SKILL.md) | Propose and approve project principles | `sdd` |
| [sdd-change](skills/sdd-change/SKILL.md) | Change requirements before downstream implementation | `sdd` |
| [sdd-status](skills/sdd-status/SKILL.md) | Read-only phase, progress, and next-step report | `sdd` |
| [feature](skills/feature/SKILL.md) | General feature planning before implementation | None |

`feature` is a general planning helper; use `sdd` for the full SDD lifecycle.
Install dependent skills together with `sdd`: the CLI does not infer dependencies
from prose instructions. Project-local installation is recommended for teams;
add `--global` only when you intentionally want a personal installation.

## Use in a destination project

1. Verify that your agent discovers the installed skills. Invoke them explicitly
   when needed; for Codex, for example: `$constitution`, `$sdd`, or
   `$sdd-status specs/001-feature-name/`.
2. Record the project's actual build, test, and quality commands in its repository
   instructions. Keep technology choices and approved principles in its
   `docs/constitution.md`, feature documents in `specs/`, and progress in `MEMORY.md`.
3. Keep shared skills unchanged where possible. Put local conventions in project
   instructions and propose reusable workflow improvements in this catalog.

## Updates and releases

Use a deliberate upgrade PR in each consuming project. Re-run installation with
the chosen newer tag or full commit, review all installed changes, verify agent
discovery, and record the source revision and installer version. Avoid automatic
upgrades from a moving branch for established projects.

This catalog uses `vMAJOR.MINOR.PATCH` tags: major for incompatible workflow,
approval, or document-contract changes; minor for compatible capabilities or new
skills; patch for corrections that preserve those contracts. Do not move a
published tag. Remove local skill overrides only after reviewing their purpose.

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

Python 3.11 or later is required only for catalog maintenance:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

The checks validate catalog packaging, naming, descriptions, companion availability,
and referenced catalog links. They do not prove agent behavior or SDD compliance.
GitHub Actions runs the same checks on pull requests, pushes, and manual dispatch.
No Python package installation is required.

## License

See [LICENSE](LICENSE) for this repository's license. Preserve the license and
applicable notices when redistributing copies of these materials.
