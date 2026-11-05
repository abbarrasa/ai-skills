# AI Skills

Set of AI skills to manage software projects using the Spec-Driven Development (SDD) methodology.

## What is Spec-Driven Development?

Spec-Driven Development (SDD) is a software engineering methodology where a clear, structured and readable specification (usually in Markdown files within the project) acts as the source of truth before writing code.
Instead of starting to program directly or giving loose, improvised orders to an artificial intelligence (a phenomenon known as vibe coding), the process is reversed: the code is the consequence of the specification, not the starting point.

### How the workflow works

Although there are variants, the basic cycle in SDD is divided into several phases:

1. Specify: You define precisely what you want to build, the objectives, business rules, limit cases and acceptance criteria.
2. Plan (Plan): You translate that intention into a technical architecture and system design (design.md).
3. Decompose (Tasks): You divide the plan into atomic tasks or small, sequential steps (tasks.md).
4. Implement & Verify: You deliver this structured documentation to a code agent (such as Claude Code, GitHub Copilot, or Cursor) to generate code and tests within those strict boundaries, verifying that it meets the original specification.

### Why has Artificial Intelligence gained so much relevance?

With the advent of advanced programming assistants, the bottleneck is no longer typing fast code, but maintaining context control.
• Avoid context drift: When an AI is given vague prompts, it tends to invent logic, break files it doesn't see, or introduce regressions.
• Limit uncertainty: By defining clear boundaries in Markdown, AI stops guessing about the architecture and works on an explicit technical contract.
• Traceability: If months later you wonder why the system makes a specific decision, the answer lives in the versioned specification in Git and not buried in a giant diff.
