# Research: 12-Factor Agents

## Summary

The "12-Factor Agents" methodology proposes a set of engineering principles for building reliable, production-ready LLM-powered applications, moving away from complex "black box" agent frameworks towards modular, code-centric designs. It emphasizes treating agents as software composed of deterministic code and LLM calls, rather than autonomous loops that "figure it out" from a single prompt. The core innovation lies in applying established software engineering practices—such as state management, structured outputs, and explicit control flow—to the unpredictable nature of LLMs, ensuring observability, debuggability, and control.

## Insights

- **Natural Language to Tool Calls**: Treat natural language inputs as triggers for structured tool calls rather than direct execution instructions.
- **Tools as Structured Outputs**: Define tools simply as structured JSON outputs from the LLM that your deterministic code executes; the LLM decides *what* to do, code controls *how*.
- **Own Your Prompts**: Do not rely on framework-hidden prompts; explicitly manage and version the prompts sent to the LLM to ensure predictability and ease of debugging.
- **Own Your Context Window**: Curate exactly what goes into the context window (prompts, history, RAG, tool outputs) to optimize for token efficiency and LLM understanding.
- **Context Engineering**: Treat the context window as your primary interface; use techniques like "compacting errors" and "pre-fetching" to manage information density.
- **Unify Execution and Business State**: Combine execution state (steps, retries) and business state (messages, tool results) into a single, serializable thread for simplicity and recoverability.
- **Launch/Pause/Resume**: Design agents with simple APIs to launch, pause (e.g., for human input), and resume execution, enabling integration with external triggers like webhooks.
- **Contact Humans with Tools**: Implement "human-in-the-loop" not as a special mode but as just another tool call (e.g., `ask_human`) that pauses execution until a response is received.
- **Own Your Control Flow**: Use explicit code (loops, switch statements) to manage the agent's flow rather than relying entirely on the LLM's internal decision-making loop.
- **Compact Errors**: When errors occur, summarize or "compact" them into the context window so the LLM knows what went wrong without cluttering the context with massive stack traces.
- **Small, Focused Agents**: Build small agents with limited scope (3-10 steps) and specific domains to maintain high performance and prevent the LLM from getting "lost" in long contexts.
- **Trigger From Anywhere**: Architect agents to be triggered by various events (Slack, email, crons, webhooks) and to respond in kind, meeting users where they are.
- **Stateless Reducer**: Model the agent's core logic as a stateless reducer function: `(current_state, event) -> new_state`, facilitating testing and reasoning about state transitions.
- **Pre-fetch Context**: If you anticipate an agent will need specific data (e.g., git tags), fetch it deterministically *before* calling the LLM, rather than waiting for the LLM to ask for it.
- **Deterministic Tool Execution**: Separate the LLM's "intent" (JSON output) from the actual execution; you can intercept, modify, or mock tool execution in your code.
- **Throw Away the DAG**: Instead of hard-coding a Directed Acyclic Graph, provide the LLM with "edges" (transitions/tools) and let it determine the path through the nodes at runtime.
- **Agents as Software**: Shift mindset from "prompting an autonomous entity" to "writing software that uses an LLM for decision nodes."
- **Single Source of Truth**: By unifying state, the "thread" becomes the single source of truth, making serialization, debugging, and UI rendering straightforward.
- **Token Efficiency**: Optimization of the context window is critical; remove unnecessary tokens and format data for maximum LLM comprehension.
- **Human Interfaces**: Unified state allows trivial conversion of agent history into human-readable formats or rich web UIs.
- **Recovery and Forking**: Serialized state allows resuming agents from any point or forking a conversation to try different paths.
- **Simplification**: Avoid complex abstractions for state management unless absolutely necessary; simple lists of events often suffice.
- **Explicit Transitions**: Define clear state transitions and let the LLM select the next state via structured output.
- **Mocking and Testing**: "Tools as structured outputs" makes it easy to mock LLM responses for unit testing the deterministic parts of the agent.
- **Separation of Concerns**: Keep the "brain" (LLM decision making) separate from the "body" (tool execution and side effects).
- **High Stakes Operations**: "Contact humans with tools" enables safe access to sensitive actions (e.g., prod deployment) by requiring explicit approval.
- **Outer Loop Agents**: Agents can be long-running processes triggered by system events, working in the background and contacting humans only when necessary.
- **Schema Aligned Parsing**: Use structured schemas (like Pydantic or JSON schemas) to force the LLM to adhere to specific output formats, reducing parsing errors.
- **Minimize "Magic"**: Avoid frameworks that hide the prompt construction or the loop logic; visibility is key to iteration and improvement.
- **Iterative Improvement**: Small, focused agents allow for easier tuning and improvement of specific capabilities without breaking the whole system.
- **Event-Driven Architecture**: The "trigger from anywhere" principle aligns agent design with modern event-driven software architectures.
- **Information Density**: Summarize previous steps or large data chunks to keep the context window "dense" with relevant information.

## Catalog

**Documentation & Factors:**
- `README.md`: Overview of the 12-Factor Agents philosophy and table of contents.
- `content/factor-01-natural-language-to-tool-calls.md`: Explains treating NL as a trigger for tool calls.
- `content/factor-02-own-your-prompts.md`: detailed guide on managing and versioning prompts.
- `content/factor-03-own-your-context-window.md`: Techniques for managing the context window (token efficiency, formatting).
- `content/factor-04-tools-are-structured-outputs.md`: Concept of tools as JSON outputs executed by code.
- `content/factor-05-unify-execution-state.md`: Merging execution and business state into a single thread.
- `content/factor-06-launch-pause-resume.md`: Designing for asynchronous, interruptible agent workflows.
- `content/factor-07-contact-humans-with-tools.md`: Implementing human-in-the-loop via standard tool patterns.
- `content/factor-08-own-your-control-flow.md`: Using code to manage the agent's high-level logic and loops.
- `content/factor-09-compact-errors.md`: Handling errors by summarizing them for the LLM context.
- `content/factor-10-small-focused-agents.md`: Architectural advice on agent scope and modularity.
- `content/factor-11-trigger-from-anywhere.md`: Integrating agents with external triggers and communication channels.
- `content/factor-12-stateless-reducer.md`: Functional programming perspective on agent state transitions.
- `content/appendix-13-pre-fetch.md`: Optimization pattern for fetching data before LLM inference.
- `content/brief-history-of-software.md`: Contextual background on software evolution leading to agents.

**Workshops:**
- `workshops/`: Contains directories for various workshops (e.g., `2025-05`, `2025-05-17`) demonstrating these principles in code (CLI, calculator tools, human approval, etc.).
