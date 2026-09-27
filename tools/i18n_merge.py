"""Merge translation keys from a JSON file into assets/i18n.js (adds or replaces).

usage: python tools/i18n_merge.py updates.json
updates.json: {"ru": {"key": "text", ...}, "it": {...}, "de": {...}}
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
path = ROOT / "assets" / "i18n.js"
s = path.read_text(encoding="utf-8")
upd = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
for lang, d in upd.items():
    start = re.search(r"\n%s: \{\n" % lang, s).end()
    end = s.index("\n}", start)
    block = s[start:end]
    for k, v in d.items():
        pair = json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False)
        pat = re.compile(r'"%s": "(?:[^"\\]|\\.)*"' % re.escape(k))
        if pat.search(block):
            block = pat.sub(lambda m: pair, block, count=1)
        else:
            block = block.rstrip() + ",\n  " + pair
    s = s[:start] + block + s[end:]
path.write_text(s, encoding="utf-8")
print("merged", {l: len(d) for l, d in upd.items()})
