# NOW

## Focus

REA plugin installed on branch `install-rea-plugin` (commit `0734d17`): skills `reverse-engineer-anything` + `crash-triage`, `rea` MCP server in `.kiro/settings/mcp.json`, pinned at `1690b63` in `.kiro/skills.lock` and `scripts/sync-skills.sh`.

## Open threads

- Branch not pushed, no PR yet. Waiting on a go.
- `rea` MCP server unverified at runtime: this sandbox's npm proxy returns 403 for `rea-agents`, and writes to the live Kiro MCP settings are denied by permission rule, so enabling it is a user step.

## Pending

- pwntools/pyelftools/Unicorn Python not present, so `inspect_recorded_crash` and `inspect_binary_layout` need `REA_PWNTOOLS_PYTHON` set before crash-triage works.

Updated: 2026-10-28T12:55:00Z
