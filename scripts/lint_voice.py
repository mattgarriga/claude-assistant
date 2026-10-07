#!/usr/bin/env python3
"""Voice linter. Usage: python3 scripts/lint_voice.py <file> [--design] [--secrets-only]   or pipe text with '-'.
Flags em dashes, emojis, banned phrases; --design also flags SDD banned words.
Always scans for secrets (rule SECRET); --secrets-only runs only that scan. Matched secret
values are masked in output. Exit 1 on any hit."""
import re, sys

PHRASES = r"hope this helps|let me know if you have (any )?questions|it'?s worth noting|(please )?don'?t hesitate to|as discussed|as mentioned|thank you for reaching out|hope (you'?re|you are) doing well|hope this (email )?finds you|trust this email finds you|i just wanted|sorry to bother|thanks in advance"
DESIGN = r"\b(robust|seamless(ly)?|leverag(e|es|ed|ing)|utiliz(e|es|ed|ing)|ensur(e|es|ed|ing)|streamlin(e|es|ed|ing)|comprehensive|as needed|where appropriate)\b"
RULES = [
    ("EM DASH", re.compile("\u2014")),
    ("SPACED EN DASH", re.compile(" \u2013 ")),
    ("EMOJI", re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")),
    ("BANNED PHRASE", re.compile(PHRASES, re.I)),
]

SECRET_RULES = [
    re.compile(r"sk-ant-[A-Za-z0-9_-]{6,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY"),
]
ASSIGN = re.compile(r"\b\w*(?:api[_-]?key|apikey|token|secret|password|passwd)\b[\"']?\s*[:=]\s*[\"']?([^\s\"']{12,})", re.I)
KEYWORD = re.compile(r"key|token|secret|password", re.I)
LONG = re.compile(r"(?<![A-Za-z0-9_/.-])[A-Za-z0-9_-]{32,}(?![A-Za-z0-9_-])")
ID_PREFIX = re.compile(r"^(?:custom|cust)[a-z]*_", re.I)


def _benign(v):
    """Values that look long but are IDs, URLs, or placeholders."""
    if ID_PREFIX.match(v) or v.lower().startswith(("http://", "https://", "<", "${", "{{", "redacted", "xxx", "your")):
        return True
    return False


def scan_secrets(text):
    """Return list of (line_number, masked_match, line_preview) for suspected secrets."""
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        found = []
        for rx in SECRET_RULES:
            found += [m.group(0) for m in rx.finditer(line)]
        for m in ASSIGN.finditer(line):
            if not _benign(m.group(1)):
                found.append(m.group(1))
        if KEYWORD.search(line):
            for m in LONG.finditer(line):
                v = m.group(0)
                if (not _benign(v) and re.search(r"\d", v) and re.search(r"[A-Za-z]", v)
                        and not re.fullmatch(r"[0-9a-fA-F]+", v)):
                    found.append(v)
        for f in dict.fromkeys(found):
            out.append((n, f[:4] + "***", line.strip().replace(f, f[:4] + "***")[:120]))
    return out


def main():
    args = [a for a in sys.argv[1:] if a not in ("--design", "--secrets-only")]
    rules = RULES + ([("DESIGN BANNED WORD", re.compile(DESIGN, re.I))] if "--design" in sys.argv else [])
    if "--secrets-only" in sys.argv:
        rules = []
    src = args[0] if args else "-"
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    hits = 0
    for n, line in enumerate(text.splitlines(), 1):
        for label, rx in rules:
            for m in rx.finditer(line):
                print(f"{label} line {n}: '{m.group(0)}' -> {line.strip()[:120]}")
                hits += 1
    for n, masked, preview in scan_secrets(text):
        print(f"SECRET line {n}: '{masked}' -> {preview}")
        hits += 1
    print("clean" if not hits else f"{hits} issue(s)")
    sys.exit(1 if hits else 0)

if __name__ == "__main__":
    main()
