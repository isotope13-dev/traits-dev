/**
 * In-memory orchestrator state for one agent run.
 * The authoritative system prompt (base policy + project policy + mode suffix).
 * NEVER pushed into messages; assembled as the leading system message on
 * every LLM call. Runtime instructions update the leading system message.
 * Task instructions are stored separately from the live assistant history.
 */
export interface RunContext {
    systemPrompt: string;
    runtimeInstructions: string[];
    task: string;
}
