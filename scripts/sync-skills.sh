#!/usr/bin/env bash
# Rebuild .kiro/skills/ from upstream. Stand-in for `npx skills add/update`
# when the npm registry is unreachable. Needs git and python3.
#
# Sources:
#   mattpocock/skills                  -> skills/*/*            (all, incl. misc + in-progress)
#   anthropics/knowledge-work-plugins  -> */skills/*, partner-built/*/skills/*
#   addyosmani/clarity                 -> clarity (SKILL.md, references, scripts, LICENSE)
#
# Name rules: a skill keeps its frontmatter name unless that name appears more
# than once or clashes with an already-installed skill; then it becomes
# <plugin>-<name>. Frontmatter `name:` is rewritten to match the folder.
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
dest="$repo_root/.kiro/skills"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

git clone -q --depth 1 https://github.com/mattpocock/skills.git "$work/mp"
git clone -q --depth 1 https://github.com/anthropics/knowledge-work-plugins.git "$work/kwp"
git clone -q --depth 1 https://github.com/addyosmani/clarity.git "$work/clarity"

rm -rf "$dest"
mkdir -p "$dest"

python3 - "$work" "$dest" <<'EOF'
import collections, os, re, shutil, sys

work, dest = sys.argv[1], sys.argv[2]

def skill_name(path):
    text = open(os.path.join(path, "SKILL.md"), encoding="utf-8").read()
    m = re.search(r"^name:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip("\"'").split("/")[0]

def install(src, name):
    target = os.path.join(dest, name)
    if os.path.exists(target):
        sys.exit(f"name clash: {name}")
    shutil.copytree(src, target, symlinks=True)
    p = os.path.join(target, "SKILL.md")
    text = open(p, encoding="utf-8").read()
    new = re.sub(r"^name:\s*.+$", f"name: {name}", text, count=1, flags=re.M)
    if new != text:
        open(p, "w", encoding="utf-8").write(new)

# 1. mattpocock/skills: every skills/<group>/<skill>/SKILL.md
mp = os.path.join(work, "mp", "skills")
for group in sorted(os.listdir(mp)):
    gdir = os.path.join(mp, group)
    if not os.path.isdir(gdir):
        continue
    for s in sorted(os.listdir(gdir)):
        sdir = os.path.join(gdir, s)
        if os.path.isfile(os.path.join(sdir, "SKILL.md")):
            install(sdir, skill_name(sdir))

# 2. knowledge-work-plugins: top-level skills of each plugin (nested sub-skills
#    stay inside their parent folder as reference material)
kwp = os.path.join(work, "kwp")
rows = []
for root, dirs, files in os.walk(kwp):
    if "/.git" in root:
        continue
    parts = os.path.relpath(root, kwp).split(os.sep)
    if "SKILL.md" in files and len(parts) >= 3 and parts[-2] == "skills":
        rows.append((parts[-3], skill_name(root), root))

existing = set(os.listdir(dest))
counts = collections.Counter(n for _, n, _ in rows)
renamed = []
for plugin, name, root in sorted(rows, key=lambda r: r[2]):
    final = f"{plugin}-{name}" if counts[name] > 1 or name in existing else name
    install(root, final)
    existing.add(final)
    if final != name:
        renamed.append(f"{os.path.relpath(root, kwp)} -> {final}")

# 3. addyosmani/clarity: single root-level skill; copy only what SKILL.md uses
cl = os.path.join(work, "clarity")
target = os.path.join(dest, "clarity")
if os.path.exists(target):
    sys.exit("name clash: clarity")
os.makedirs(target)
for item in ("SKILL.md", "LICENSE", "references", "scripts"):
    src = os.path.join(cl, item)
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(target, item))
    else:
        shutil.copy2(src, target)

print(f"installed {len(os.listdir(dest))} skills")
for r in renamed:
    print("  renamed", r)
EOF

for r in mp kwp clarity; do
  printf '%s %s\n' "$r" "$(git -C "$work/$r" rev-parse --short HEAD)"
done > "$repo_root/.kiro/skills.lock"
echo "pinned commits written to .kiro/skills.lock"
