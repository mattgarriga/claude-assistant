#!/usr/bin/env python3
"""Voice linter. Usage: python3 scripts/lint_voice.py <file> [--design]   or pipe text with '-'.
Flags em dashes, emojis, banned phrases; --design also flags SDD banned words. Exit 1 on any hit."""
import re, sys

PHRASES = r"hope this helps|let me know if you have (any )?questions|it'?s worth noting|(please )?don'?t hesitate to|as discussed|as mentioned|thank you for reaching out|hope (you'?re|you are) doing well|hope this (email )?finds you|trust this email finds you|i just wanted|sorry to bother|thanks in advance"
DESIGN = r"\b(robust|seamless(ly)?|leverag(e|es|ed|ing)|utiliz(e|es|ed|ing)|ensur(e|es|ed|ing)|streamlin(e|es|ed|ing)|comprehensive|as needed|where appropriate)\b"
RULES = [
    ("EM DASH", re.compile("\u2014")),
    ("SPACED EN DASH", re.compile(" \u2013 ")),
    ("EMOJI", re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")),
    ("BANNED PHRASE", re.compile(PHRASES, re.I)),
]

def main():
    args = [a for a in sys.argv[1:] if a != "--design"]
    rules = RULES + ([("DESIGN BANNED WORD", re.compile(DESIGN, re.I))] if "--design" in sys.argv else [])
    src = args[0] if args else "-"
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    hits = 0
    for n, line in enumerate(text.splitlines(), 1):
        for label, rx in rules:
            for m in rx.finditer(line):
                print(f"{label} line {n}: '{m.group(0)}' -> {line.strip()[:120]}")
                hits += 1
    print("clean" if not hits else f"{hits} issue(s)")
    sys.exit(1 if hits else 0)

if __name__ == "__main__":
    main()
