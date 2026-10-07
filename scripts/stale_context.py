#!/usr/bin/env python3
"""Local-only context freshness report. No connectors.

Usage: python3 scripts/stale_context.py [--days 30]
Flags a client when any core file has no commit in N days, or the context is thin
(no contacts, no decisions, empty tool IDs, projects with no status lines).
"""
import datetime, glob, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DAYS = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 30
TODAY = datetime.date.today()


def age(path):
    r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    d = datetime.date.fromisoformat(r) if r else datetime.date.fromtimestamp(os.path.getmtime(os.path.join(ROOT, path)))
    return (TODAY - d).days


def rows(text, section):
    m = re.search(rf"^## {re.escape(section)}.*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return [l for l in (m.group(1).splitlines() if m else []) if l.startswith("|") and not re.match(r"^\|[-| ]+\|$", l)][1:]


out = []
for d in sorted(glob.glob(os.path.join(ROOT, "clients", "*", ""))):
    slug = os.path.basename(d.rstrip("/"))
    if slug.startswith("_"):
        continue
    rel = f"clients/{slug}"
    c = open(os.path.join(d, "client.md")).read()
    contacts = len(rows(c, "Contacts"))
    empty_ids = sum(1 for l in rows(c, "Tool IDs") if re.match(r"^\|[^|]*\|\s*\|?\s*$", l) or l.rstrip().endswith("|  |"))
    decisions = len(re.findall(r"^\d{4}-\d{2}-\d{2} \|", open(os.path.join(d, "decisions.md")).read(), re.M))
    ages = [age(f"{rel}/{f}") for f in ("client.md", "decisions.md", "internal.md")]
    projects = glob.glob(os.path.join(d, "projects", "*", "project.md"))
    thin = [os.path.basename(os.path.dirname(p)) for p in projects if "(as of" not in open(p).read() and "Status" in open(p).read() and not re.search(r"## Status[^\n]*\n- \S", open(p).read())]
    flags = []
    if max(ages) > DAYS: flags.append(f"file untouched {max(ages)}d")
    if contacts == 0: flags.append("no contacts")
    if decisions == 0: flags.append("no decisions")
    if empty_ids: flags.append(f"{empty_ids} blank tool IDs")
    if thin: flags.append("thin projects: " + ", ".join(thin))
    out.append((slug, min(ages), contacts, decisions, len(projects), "; ".join(flags) or "ok"))

print("| Client | Newest file age (d) | Contacts | Decisions | Projects | Flags |")
print("|---|---|---|---|---|---|")
for r in sorted(out, key=lambda r: (r[5] == "ok", r[0])):
    print("| " + " | ".join(str(x) for x in r) + " |")
