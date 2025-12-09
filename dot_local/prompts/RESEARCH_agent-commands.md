# Research: Agent Commands

## Summary

This repository is a collection of pragmatic, command-based prompts and "skills" designed to be used with an AI agent (specifically Claude) to automate software engineering tasks. Instead of abstract frameworks, it uses direct markdown instructions that define specific "commands" like `/handoff`, `/pickup`, and `/make-release`, acting as standard operating procedures for the agent. The innovation lies in formalizing the "human-to-agent" protocol through simple, documented commands that encapsulate complex workflows, state management (via handoff files), and tool interactions (tmux, browser).

## Insights

- **Command-Based Protocol**: Defines a clear interaction model where the user issues specific "slash commands" (e.g., `/handoff`) that map to detailed markdown instructions for the agent.
- **Explicit Handoffs**: Implements a `/handoff` command to formalize state preservation, requiring the agent to summarize the current context, technical decisions, and pending tasks into a file.
- **Session Continuity**: The `/pickup` command allows an agent to resume work from a serialized state file, enabling long-running tasks to span multiple sessions or agents.
- **Purpose-Driven Summaries**: Handoffs are not just logs; they must have a specific "purpose" to guide the next agent, ensuring continuity of *intent*, not just data.
- **Slug-Based Naming**: Uses human-readable "slugs" (e.g., `fix-issue-42`) to name handoff files, making them easy for humans to identify and reference.
- **Structured Handoff Plan**: The handoff instruction mandates a specific XML-like structure (`<analysis>`, `<plan>`) to force the agent to "think" before writing the final markdown file.
- **Release Automation**: The `/make-release` command encapsulates the complex logic of semantic versioning, changelog updates, and git tagging into a single agent-driven workflow.
- **Safety First in Releases**: The release process explicitly stops before pushing, forcing a human review step ("Do NOT automatically push"), balancing automation with safety.
- **Changelog Management**: The `/update-changelog` command teaches the agent how to read git logs and write meaningful, user-centric changelog entries, filtering out noise.
- **Skill Definitions**: Defines "Skills" (Browser, tmux) as markdown files containing metadata (name, description) and usage instructions, similar to MCP but simpler.
- **Remote Control Browser**: The browser skill uses a custom toolset (`tools/nav.js`, `tools/pick.js`) to drive a real Chrome instance via CDP, preferring this over generic browser APIs.
- **Interactive Element Picking**: Includes a specific tool (`pick.js`) for the agent to ask the user to visually select elements on a screen, solving the "how to click the right thing" problem.
- **Tmux as a Sandbox**: Uses `tmux` as a robust, persistent sandbox for running CLI tools (Python, gdb), allowing the agent to observe output and send keystrokes reliably.
- **Private Sockets**: The tmux skill emphasizes using private sockets to isolate agent sessions from the user's personal terminal sessions.
- **Monitoring Instructions**: The tmux skill mandates that the agent *always* tell the user how to attach to the session (`tmux -S ... attach`), ensuring observability.
- **Polling for Prompts**: The tmux skill includes a helper (`wait-for-text.sh`) to robustly handle the asynchronous nature of CLI tools, preventing the agent from typing before the prompt is ready.
- **Environment Control**: Explicitly sets environment variables like `PYTHON_BASIC_REPL=1` to ensure tools behave predictably (no fancy readline features) for the agent.
- **Literal Sends**: Advises using "literal sends" in tmux to avoid shell expansion issues, showing a deep understanding of the pitfalls of programmatic terminal interaction.
- **Analysis Tags**: Uses `<analysis>` tags in prompts to force "Chain of Thought" reasoning before generating the final artifact or taking action.
- **Baseline Versioning**: The changelog command handles the logic of finding the "baseline" version (last tag) to generate a diff, automating a common manual step.
- **Instruction Tuning**: The README notes that these commands "do not work without tuning," acknowledging that agent prompts often need customization for specific project contexts.
- **Tool-Specific Scripts**: The repository doesn't just rely on the LLM; it provides helper scripts (JS for browser, bash for tmux) that serve as the "hands" for the agent's "brain."
- **User-Centric Changelogs**: Explicit guidelines for the agent to write "good" changelog entries (focus on features, ignore typos), improving the quality of generated documentation.
- **Hybrid Automation**: The workflows are designed to be "human-in-the-loop" by default (e.g., asking for purpose if missing, asking for confirmation before push).
- **In-Context Learning**: The commands act as few-shot examples or detailed system instructions that are injected into the context when the specific keyword is used.
- **State Serialization**: The "handoff" concept effectively creates a checkpoint system for agent memory, decoupled from the specific chat interface or model provider.
- **Visual Nav**: The browser skill supports screenshots, allowing the agent to "see" the state of the web page, crucial for debugging and verification.
- **Structured Arguments**: Commands parse arguments (e.g., `$ARGUMENTS`), allowing for parameterization of the agent's task (e.g., `/handoff "implement auth"`).
- **Defensive Prompting**: Instructions include constraints like "If no purpose was provided... you must STOP IMMEDIATELY," preventing the agent from hallucinating a goal.
- **Inspiration vs. Prescription**: The "specific" folder explicitly states these are "mostly just for inspiration," encouraging users to adapt the patterns rather than copy the code blindly.

## Catalog

**Documentation & Common Commands:**
- `README.md`: Overview of the repository and the "agent command" concept.
- `common/handoff.md`: Prompt for creating a session handoff (summary + plan).
- `common/pickup.md`: Prompt for resuming a session from a handoff file.

**Specific Commands (Project-Specific Examples):**
- `specific/make-release.md`: Prompt for automating the release process (version bump, tag, commit).
- `specific/update-changelog.md`: Prompt for generating changelog entries from git history.

**Skills (Tool Definitions):**
- `skills/web-browser/SKILL.md`: Documentation for the web browser control skill.
- `skills/web-browser/tools/`: Directory containing JS scripts (`start.js`, `nav.js`, `eval.js`, `pick.js`, `screenshot.js`) for CDP interaction.
- `skills/tmux/SKILL.md`: Documentation for the tmux control skill.
- `skills/tmux/tools/`: Directory containing helper scripts (e.g., `wait-for-text.sh`) for robust tmux interaction.
