---
inclusion: always
---

# Use skills automatically

Every folder in `.kiro/skills/` is a skill (263, from `mattpocock/skills` and `anthropics/knowledge-work-plugins`; commits pinned in `.kiro/skills.lock`).

- Before starting any task, check whether a skill's description matches it. If one does, load and follow it without being asked. If several match, use the most specific.
- A user typing `/<skill-name>` means: load that skill now.
- `ask-matt` routes between the engineering skills; `smb-router` routes between the small-business skills.
- Skills that write to connected tools (CRM, mail, ledger, payments) still need the user's explicit approval before any external write or send.
- Refresh skills with `scripts/sync-skills.sh`, never by hand-editing `.kiro/skills/`.

## Agent skills

### Issue tracker

GitHub Issues on this repo, via REST (`gh api`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default five labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the root. See `docs/agents/domain.md`.
