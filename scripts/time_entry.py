#!/usr/bin/env python3
"""Daily time entry helper for Matt's NetSuite time import.

parse <notes.txt>            -> JSON entries from the OneNote day block
build <final.json> --date D  -> validates, rounds to 0.25, reconciles, writes time/D.csv
Resolution and client-safe memo rewriting are done by Claude between the two steps.
"""
import csv, json, os, re, sys, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TIME = os.path.join(ROOT, "time")
HEAD = ["Date", "Employee", "Name", "Case/Task/Event", "Item", "Duration (Decimal)", "Note"]
LINE = re.compile(r"^\s*(?P<client>[^-:]+?)\s+-\s+(?P<label>.+?):\s*(?P<hours>\d*\.?\d+)\s*\|?\s*$")


def q(x):
    return round(float(x) * 4) / 4


def parse(text):
    entries, cur = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = LINE.match(line)
        if m:
            cur = {"client": m["client"].strip(), "label": m["label"].strip(),
                   "hours_raw": float(m["hours"]), "tasks": []}
            entries.append(cur)
        elif line.startswith("*") and cur is not None:
            cur["tasks"] += [t.strip() for t in line.lstrip("* ").split("|") if t.strip()]
        else:
            entries.append({"unparsed": line})
    return entries


def reconcile(rows):
    for r in rows:
        r["hours"] = q(r["hours"])
    raw_total = sum(float(r.get("hours_raw", r["hours"])) for r in rows)
    target = q(raw_total)
    diff = round(target - sum(r["hours"] for r in rows), 2)
    if diff:
        max(rows, key=lambda r: r["hours"])["hours"] += diff
    return target


def build(rows, date, employee="Matthew Garriga"):
    errs = []
    for r in rows:
        if r.get("hours") in (None, "") and r.get("hours_raw") not in (None, ""):
            r["hours"] = r["hours_raw"]
    for i, r in enumerate(rows, 1):
        for k in ("project", "task", "item", "memo", "hours"):
            if r.get(k) in (None, ""):
                errs.append(f"entry {i} ({r.get('client')} - {r.get('label')}): missing {k}")
    if errs:
        return None, errs
    ledger_path = os.path.join(TIME, "exported.json")
    ledger = json.load(open(ledger_path)) if os.path.exists(ledger_path) else {}
    if date in ledger:
        return None, [f"{date} already exported to {ledger[date]['file']}; delete its ledger entry to redo"]
    total = reconcile(rows)
    d = datetime.datetime.strptime(date, "%Y-%m-%d")
    out = os.path.join(TIME, f"{date}.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        for r in rows:
            w.writerow([f"{d.month}/{d.day}/{d.year}", employee, r["project"], r["task"], r["item"], f"{r['hours']:g}", r["memo"]])
    ledger[date] = {"file": os.path.relpath(out, ROOT), "total": total, "rows": len(rows)}
    json.dump(ledger, open(ledger_path, "w"), indent=2)
    return out, [f"{len(rows)} rows, {total:g} hours"]


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "parse":
        ents = parse(open(a[1]).read())
        print(json.dumps({"entries": ents, "total_raw": sum(e.get("hours_raw", 0) for e in ents)}, indent=1))
    elif len(a) >= 4 and a[0] == "build" and a[2] == "--date":
        out, msgs = build(json.load(open(a[1])), a[3])
        print("\n".join(msgs))
        sys.exit(0 if out else 1)
    else:
        print(__doc__)
        sys.exit(2)
