#!/usr/bin/env python3
"""Pattern Recognition Utility (URCM toy)
Scans text for simple signals: claims, contradictions (very naive), and operator mentions.
"""
import argparse, json, re, sys

OPS = ["Ĉ","Ŝ","B̂","R̂","E","F","T","H","D","M","X","N"]
CLAIM_RE = re.compile(r"\b(we|i) (show|prove|demonstrate|find|claim)\b", re.I)
NEG_RE = re.compile(r"\b(no|not|never|cannot|can't|won't)\b", re.I)

def analyze(text: str):
    ops = [op for op in OPS if op in text]
    claims = len(CLAIM_RE.findall(text))
    negs = len(NEG_RE.findall(text))
    contradictions = max(0, claims - negs//2)  # toy heuristic
    return {"operators_detected": ops, "claims": claims, "neg_markers": negs, "contradiction_score": contradictions}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f","--file")
    ap.add_argument("-t","--text")
    args = ap.parse_args()
    if not (args.file or args.text):
        print("Provide --file or --text", file=sys.stderr)
        sys.exit(2)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = args.text
    print(json.dumps(analyze(text), indent=2))

if __name__ == "__main__":
    main()
