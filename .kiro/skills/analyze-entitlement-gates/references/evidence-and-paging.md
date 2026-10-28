# Evidence, views, citations

- **Summary first.** `inspect_analysis_view` with `view: {kind: "summary"}` over saved
  evidence. Page into function-level detail only where the graph points.
- **Retained references.** When the server advertises retained evidence, keep evidence
  ids and page them. When it does not, keep complete inline Evidence.
- **Citation format** in every claim:
  `<artifact> · <tool> · <evidence id / address / key> · <limitation>`
  Example: `MyApp 4.2.1 · procedure_pseudo_code · 0x1007d4 · sym stripped, inferred name`
- **Preserve digests** across pages (source digest, byte hash, tool version).
- **Declare gaps** exactly as REA does: unresolved dynamic IPC channel names,
  `resource_constraint` members, missing engines, unknown headers. Never convert "not
  found" into "not present".
- **Report template**: `assets/gate-report.md`.
