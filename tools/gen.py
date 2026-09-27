"""Generate one image from assets/PROMPTS.md with Gemini.

usage: python tools/gen.py <number> [--model M] [--ref path] [--extra "text"]
Saves assets/raw/gen/<name>-vN.png (N increments on every run).
The key is read from .env and never printed.
"""
import argparse, base64, json, pathlib, re, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "raw" / "gen"


def key():
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("GEMINI_API_KEY missing in .env")


def prompts():
    text = (ROOT / "assets" / "PROMPTS.md").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^### (\d+)\. `([\w-]+)\.webp`.*?\n(.*?)(?=^### |^---|\Z)", text, re.S | re.M):
        body = m.group(3).strip()
        ref = re.match(r"\*\(reference: image (\d+)\)\*\s*", body)
        out[int(m.group(1))] = {"name": m.group(2), "ref": ref and int(ref.group(1)),
                                "prompt": body[ref.end():] if ref else body}
    return out


def latest(name):
    files = sorted(OUT.glob(f"{name}-v*.png"), key=lambda p: int(p.stem.rsplit("-v", 1)[1]))
    return files[-1] if files else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("--model", default="gemini-3.1-flash-image")
    ap.add_argument("--ref", help="reference image path (default: latest version of the referenced prompt)")
    ap.add_argument("--extra", default="", help="extra instructions appended to the prompt")
    ap.add_argument("--aspect", default=None)
    a = ap.parse_args()
    p = prompts()[a.n]
    OUT.mkdir(parents=True, exist_ok=True)
    parts = []
    ref = pathlib.Path(a.ref) if a.ref else (p["ref"] and latest(prompts()[p["ref"]]["name"]))
    if p["ref"] and not ref:
        sys.exit(f"reference image {p['ref']} not generated yet")
    if ref:
        parts.append({"inline_data": {"mime_type": "image/png", "data": base64.b64encode(ref.read_bytes()).decode()}})
        parts.append({"text": "Reference image above. " + p["prompt"] + (" " + a.extra if a.extra else "")})
    else:
        parts.append({"text": p["prompt"] + (" " + a.extra if a.extra else "")})
    aspect = a.aspect or ("16:9" if p["name"].startswith(("still", "linen", "petals")) else "1:1")
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect, "imageSize": "2K"}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent",
        data=json.dumps(body).encode(), headers={"x-goog-api-key": key(), "Content-Type": "application/json"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read()[:500].decode(errors='replace')}")
    img = [x["inlineData"]["data"] for c in d.get("candidates", []) for x in c.get("content", {}).get("parts", []) if "inlineData" in x]
    if not img:
        sys.exit("no image returned: " + json.dumps(d)[:500])
    prev = latest(p["name"])
    v = int(prev.stem.rsplit("-v", 1)[1]) + 1 if prev else 1
    path = OUT / f"{p['name']}-v{v}.png"
    path.write_bytes(base64.b64decode(img[0]))
    print(path.relative_to(ROOT), "ref=" + (ref.name if ref else "-"), d.get("usageMetadata", {}).get("totalTokenCount"))


if __name__ == "__main__":
    main()
