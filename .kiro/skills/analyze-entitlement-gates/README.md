# analyze-entitlement-gates

An installable Agent Skill (agentskills.io / Hermes-compatible) for locating,
explaining, proving, and documenting how an app **you own or are authorized to test**
gates premium features, using REA's MCP tools.

It covers iOS `.ipa`, Android `.apk`/`.aab`, Electron/JavaScript, .NET, native
binaries, and web paywalls: target routing, string/xref gate hunting, decompile-to-
confirm, runtime proof (Frida/GDB/Rizin/ADB), differential replay, evidence bundling,
and reporting.

## Two safety properties kept on purpose

1. **Authorization gate (SKILL.md step 0).** Scope is declared in `assets/scope.json`
   before any target-touching call. Obviously-not-yours targets stop there.
2. **Confirmation on side effects (step 5+).** Anything that runs, installs,
   instruments, or mutates a target is confirmed before it runs and logged after.
   Read-only static analysis needs no prompt.

`assets/mcp.json` ships with auto-approve **off** and only documented REA schema
switches set. This skill is for understanding and rebuilding your own software,
interoperability research, and authorized assessment. It is not for redistributing
patched builds or bypassing payment in production.

## Layout

```
analyze-entitlement-gates/
├── SKILL.md
├── references/   target-routing, ios-ipa, android-apk, javascript-electron-web,
│                 native-desktop, runtime-instrumentation, evidence-and-paging,
│                 recovery-and-safety
├── scripts/      00-install · 01-doctor · 02-triage-ipa · 03-hunt-gate-macho ·
│                 04-triage-apk · 05-triage-electron · 06-diff-replay ·
│                 07-summarize-evidence · 08-frida-gate-probe.js
└── assets/       scope.json, mcp.json, gate-report.md, prompts/
```

## Install

Drop the directory in `~/.hermes/skills/`, then invoke `/analyze-entitlement-gates`
or ask naturally. References load on demand; scripts run when needed.

## Requirements

Hermes Agent v0.22.1+ with the `rea` plugin; Node.js 22.19+/24.11+/26+ and npx on
PATH. BYO Ghidra/JDK, Hopper, IDA, JADX+Java, Frida, GDB/Rizin, TShark, WABT, Binwalk.
