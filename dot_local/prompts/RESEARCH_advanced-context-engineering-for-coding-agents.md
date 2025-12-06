# Research: Advanced Context Engineering for Coding Agents

## Summary

This document articulates a methodology for using AI coding agents effectively in large, brownfield codebases, challenging the notion that current models are only good for small or greenfield projects. The core technique is "Frequent Intentional Compaction," which involves structuring the development workflow into discrete phases of Research, Plan, and Implement, with rigorous human review and context resetting (compaction) between steps. This approach shifts the focus from "vibing" with a chatbot to a disciplined engineering craft where context management and mental alignment are the primary drivers of productivity and code quality.

## Insights

- **Frequent Intentional Compaction**: The central thesis is to manage the context window by frequently pausing to "compact" progress into structured artifacts (markdown files) and resetting the session.
- **Research-Plan-Implement Loop**: Divides coding tasks into three distinct phases: Research (understanding the code), Plan (outlining steps and verification), and Implement (executing the plan).
- **Context as a Stateless Function**: Treats the LLM as a stateless function where the quality of output is entirely dependent on the quality of the input context.
- **Context Optimization Goals**: Optimize context for Correctness, Completeness, Size, and Trajectory (in that order); missing info is better than incorrect info.
- **Human Leverage**: Focus human effort on reviewing the *research* and the *plan* rather than just the code; a bad plan leads to hundreds of bad lines of code.
- **Specs as Code**: Shifts the source of truth from the code itself to the specs (plans/research docs), similar to how source code is the truth for compiled binaries.
- **Mental Alignment**: The primary goal of the process is to keep the team aligned on *what* is being built and *why*, especially when AI generates code faster than humans can read it.
- **Subagents for Context Control**: Uses subagents not for role-playing but to perform searches and summarizations in a separate context window, keeping the main context clean.
- **Intentional Compaction via Subagents**: Subagents should return structured summaries that "compact" their findings, preventing noise from polluting the main thread.
- **Plan-Driven Development**: Writing a detailed implementation plan with specific testing steps *before* writing code dramatically increases success rates.
- **Research First**: Forcing a research phase prevents the AI from hallucinating solutions based on assumptions; it must "read" the code before it "writes."
- **Context Window Economics**: With a limited context window (~170k tokens), "spending" tokens on high-value information (relevant code, specific docs) is an engineering constraint.
- **The "Ralph Wiggum" Technique**: Mentions a "hilariously dumb" but effective technique of running an agent in an infinite loop with a static prompt to solve problems.
- **Worktree Usage**: Suggests using git worktrees primarily for the *implementation* phase to keep the main branch clean for research and planning.
- **Documentation as Artifacts**: The artifacts generated (research docs, plans) serve as lasting documentation for the codebase, aiding future understanding.
- **Brownfield Viability**: Explicitly targets "brownfield" (existing, complex) codebases, proving success with examples like a 300k LOC Rust project.
- **Utilization Range**: Recommends keeping context utilization in the 40-60% range to maintain model performance and prevent "forgetting."
- **High-Leverage Review**: Reviewing a 200-line plan is feasible and high-leverage; reviewing a 2000-line generated PR is low-leverage and error-prone.
- **Avoid "Vibe Coding"**: Moves away from unstructured, chatty interactions ("vibing") towards rigid, artifact-based workflows.
- **Verification Steps**: Plans must include precise verification steps for each phase, ensuring that the agent (and human) knows when a step is actually done.
- **Compaction via Commit Messages**: Suggests using commit messages as a form of compaction, summarizing changes for the next context window.
- **The "Slop" Problem**: Acknowledges that unstructured AI use leads to "slop" (rework, tech debt) and aims to eliminate it through rigor.
- **Spec-Driven Development**: Aligns with the idea that in the future, developers will interact mostly with specs, not the underlying implementation details.
- **Stateless Reducer Mindset**: Views the agent's progress as a series of state transitions reduced from the context and current events.
- **Debugging as Research**: Treats debugging not as a random trial-and-error loop but as a "Research" task to find the root cause before attempting a fix.
- **Context Trajectory**: Managing the "trajectory" of the context—ensuring it points towards the solution—is a key part of the engineering craft.
- **Expertise Requirement**: Acknowledges that for truly hard problems, at least one human expert with deep codebase knowledge is still necessary (e.g., the Hadoop/Parquet failure).
- **Tooling Over Models**: Argues that better workflows (context engineering) yield better results today than waiting for "smarter models."
- **Post-IDE IDE**: Envisions a future development environment ("CodeLayer") designed specifically for this spec-first, agentic workflow.
- **Cost Acceptance**: Acknowledges that this high-context approach is expensive (e.g., $12k/month for a small team) but implies the productivity gain justifies it.

## Catalog

**Documentation:**
- `ace-fca.md`: The primary research document (a blog post/article) detailing the "Advanced Context Engineering" methodology.

**Mentioned Concepts/Artifacts (Conceptual Catalog):**
- **Research Doc**: A markdown file summarizing codebase understanding, relevant files, and information flow.
- **Plan Doc**: A markdown file outlining implementation steps, edits, and verification procedures.
- **Implementation Doc**: A markdown file tracking the progress of the plan execution.
- **Compaction Prompt**: A prompt used to summarize the current state into a `progress.md` file.
- **Generic Subagent**: A standard agent configuration used for purely informational tasks (searching/reading).
- **Custom Subagent**: A specialized agent config (like `research_codebase.md`) tailored for specific tasks.
