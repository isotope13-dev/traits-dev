"""Repo intake, text a person cannot see and text written for an AI agent instead of a person.

    text.invisible_unicode     zero-width, bidirectional-override and tag characters inside a text file
    text.agent_instructions    wording aimed at an AI coding agent: drop your instructions, hide this from the user,
                               send keys somewhere, run this command

Read from README / docs, agent instruction files (CLAUDE.md, AGENTS.md, GEMINI.md, SKILL.md, .cursorrules, Cursor
rules, Copilot instructions, MCP configs) and the comments of source files. Where the text sits decides the
confidence: inside an HTML comment or an agent file is higher than visible README prose; a line that is plainly
discussing prompt injection (quoting the phrase, "detects", "example") is lowered one step.
"""
