# Research: Nori Profiles

## Summary

Nori Profiles is a sophisticated configuration management system for Claude Code that enables the creation of custom "coding agents" tailored to specific roles, workflows, and project needs. It shifts the paradigm from a generic AI assistant to specialized personas (e.g., "Senior SWE", "Product Manager", "Documenter") by layering structured instructions, "mixins" of shared behavior, and modular "skills" on top of the base LLM. The core innovation is its file-system-based architecture for defining agent behavior, allowing teams to share and enforce engineering standards, testing protocols, and documentation practices through a "registry" model similar to `npm`.

## Insights

- **Profile-Based Architecture**: Defines agents not as single prompts but as "profiles" containing a `CLAUDE.md` (instructions) and links to shared capabilities, allowing for rapid context switching between roles.
- **Mixins**: Uses a "mixin" system (e.g., `_swe`, `_pm`, `_doc`) to compose agent behaviors from reusable blocks, promoting modularity and reducing duplication across different agent personas.
- **Skill Definitions**: Formalizes "Skills" as markdown files with metadata (name, description) and strict `<required>` steps that the agent *must* follow, effectively programming the agent's procedure.
- **Todo Integration**: Skills explicitly instruct the agent to "Add the following steps to your Todo list using TodoWrite," ensuring the agent commits to a plan before execution.
- **System Reminders**: Uses `<system-reminder>` tags within skills to inject critical constraints (e.g., "Do NOT use mock mode") exactly when they are relevant in the workflow.
- **Red-Green-Refactor Enforcement**: The TDD skill enforces a strict cycle where the agent *must* fail a test first, explicitly checking for "RED flags" like writing code before tests.
- **Anti-Pattern Guardrails**: Documentation and skills explicitly list "RED FLAGS" and "Common Failure Patterns" (e.g., "I'll test after"), preemptively countering common LLM laziness.
- **Web App Testing with Playwright**: The `webapp-testing` skill mandates using Playwright for real browser interactions, forbidding mocks to ensure end-to-end verification.
- **Visual Verification**: Requires the agent to run Playwright in non-headless mode for a "final demonstration" to the user, bridging the gap between automated testing and human trust.
- **Root Cause Tracing**: Defines a specific skill for debugging that forces a systematic approach rather than random guessing, likely using log analysis and hypothesis testing.
- **Documentation as Code**: Treats documentation updates as a core engineering task, with specific subagents (`nori-change-documenter`) dedicated to keeping docs in sync with code.
- **Registry Model**: Introduces a "paid" registry feature for teams to upload and download profiles, facilitating the sharing of "best practice" agents across an organization.
- **Status Line Integration**: Enhances the CLI experience with a custom status line showing context usage, cost, and the active profile, keeping the user aware of agent "overhead."
- **Hooks System**: Implements hooks to trigger specific behaviors or checks at different points in the agent's lifecycle, allowing for dynamic adaptation.
- **Worktree Support**: Explicitly handles git worktrees in skills, acknowledging complex developer setups that standard agents often miss.
- **Six-Checkpoint Workflow**: The "Senior SWE" profile follows a rigid 6-step process (Verification -> Research -> Plan -> TDD -> Implementation -> Verification) to ensure quality.
- **Subagents for Specialization**: Uses "subagents" (e.g., `nori-knowledge-researcher`, `nori-codebase-locator`) to offload specific cognitive tasks, preventing context pollution in the main thread.
- **Slash Command Abstractions**: Maps complex behaviors to simple slash commands (`/nori-debug`, `/nori-init-docs`), making advanced capabilities accessible.
- **Local NoriDocs**: Maintains a local documentation store that the agent actively manages, ensuring it has a "long-term memory" of project-specific knowledge.
- **Codebase Pattern Finder**: A specific subagent designed to identify existing patterns in the codebase, encouraging consistency in new code.
- **Interactive Profile Creation**: Includes a `/nori-create-profile` command where the agent interviews the user to build a custom profile, lowering the barrier to entry.
- **Dependency Management**: The TDD skill forces the agent to write a "Plan Document" with a specific footer, ensuring every plan addresses testing and implementation details.
- **Virtual Environment Enforcement**: Explicitly commands the agent to use virtual environments for Python, preventing system pollution.
- **Mocking Prohibition**: Multiple skills (TDD, Webapp Testing) explicitly forbid "testing mocks," pushing the agent towards high-value integration tests.
- **Plan Footer Standard**: Mandates a consistent footer structure for all plans, making it easier for the user (and other agents) to parse the agent's intent.
- **Cost Awareness**: The status line includes conversation cost, adding a dimension of economic awareness to the agent's operation.
- **Self-Correction Loops**: The debugging skill prescribes a loop of "Add logs -> Run -> Analyze -> Update" until the bug is fixed, modeling human debugging behavior.
- **YAGNI/DRY Principles**: Embeds software engineering principles directly into the "Remember" sections of skills, keeping the agent aligned with best practices.
- **Explicit File Paths**: Demands "Exact file paths always," reducing the ambiguity that often leads to agents creating files in the wrong places.
- **Console UI**: The project includes a "Console" visual (referenced in README) implying a rich terminal user interface beyond simple text streaming.
- **Community Inspiration**: Acknowledges influence from "Jesse Vincent" and "humanlayer," showing it builds upon a shared body of knowledge in agent engineering.

## Catalog

**Documentation & CLI:**
- `README.md`: Introduction, installation, and usage guide.
- `docs.md`: General documentation links.
- `src/cli/commands/docs.md`: Documentation for CLI commands.

**Profiles (Persona Definitions):**
- `src/cli/features/profiles/config/senior-swe/CLAUDE.md`: Instructions for the "Senior SWE" profile.
- `src/cli/features/profiles/config/product-manager/CLAUDE.md`: Instructions for the "Product Manager" profile.
- `src/cli/features/profiles/config/documenter/CLAUDE.md`: Instructions for the "Documenter" profile.

**Mixins (Shared Capabilities):**
- `_swe/`: Engineering skills (TDD, debugging, planning).
- `_docs/`: Documentation skills (updating docs, initial documentation).
- `_base/`: Core skills (switching profiles, registry interactions).
- `_paid/`: Premium features (knowledge researcher, recall).

**Skills (Specific Workflows):**
- `_swe/skills/test-driven-development/SKILL.md`: Strict TDD workflow.
- `_swe/skills/webapp-testing/SKILL.md`: Playwright-based testing workflow.
- `_swe/skills/systematic-debugging/SKILL.md`: Structured debugging process.
- `_swe/skills/writing-plans/SKILL.md`: Planning template and requirements.
- `_swe/skills/handle-large-tasks/SKILL.md`: Strategy for breaking down big tasks.
- `_swe/skills/root-cause-tracing/SKILL.md`: Deep dive debugging skill.
- `skills/web-browser/SKILL.md`: (in other repo, but concept applies here too).

**Subagents:**
- `nori-codebase-pattern-finder.md`: Agent for finding code patterns.
- `nori-knowledge-researcher.md`: Agent for researching knowledge.
- `nori-change-documenter.md`: Agent for documenting changes.

**Slash Commands:**
- `nori-toggle-session-transcripts.md`: Command to toggle transcripts.
- `nori-switch-profile.md`: Command to switch profiles.
