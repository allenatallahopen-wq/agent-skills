# agent-skills

Kiro workspace config: identity (`SOUL.md`), memory (`memory/`, `NOW.md`), and 323 auto-used skills in `.kiro/skills/`.

- Always-on steering: `.kiro/steering/soul.md`, `.kiro/steering/skills.md`
- Update skills: `./scripts/sync-skills.sh`
- Sources: [mattpocock/skills](https://github.com/mattpocock/skills), [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), [NousResearch/hermes-official-plugins](https://github.com/NousResearch/hermes-official-plugins) `rea/`, [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) `skills/` (see their licenses)

## REA plugin

`reverse-engineer-anything` and `crash-triage` come from the Hermes [REA plugin](https://github.com/NousResearch/hermes-official-plugins/tree/main/rea) (MIT), vendored at commit `1690b63`. They need REA's MCP server, declared in `.kiro/settings/mcp.json` as `npx -y rea-agents@6.7.0 mcp`.

- Node.js 22.19+, 24.11+ or 26+ (not 23 or 25), with `npx` on `PATH`.
- Core dumps and offline ELF layout (`inspect_recorded_crash`, `inspect_binary_layout`) need a Python with pwntools 4.15.0, pyelftools 0.33 and Unicorn 2.1.2. Add `"REA_PWNTOOLS_PYTHON": "/path/to/venv/bin/python"` to the server's `env` block; a value exported only in your shell does not reach the server.
- Native decompilation, Android code, firmware extraction and the packet/debugger formats need their own engines (Ghidra + JDK, JADX + Java, Binwalk/Unblob, TShark, Rizin, Frida, ...). REA never installs them, and neither should the agent. Engines on `PATH` work as is; engines located through an environment variable need that variable in the same `env` block.
