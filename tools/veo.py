"""Generate a short video with Veo from a prompt (and optionally a first-frame image).

usage: python tools/veo.py <out.mp4> "<prompt>" [--image first.png] [--model veo-3.1-lite-generate-preview]
       [--aspect 16:9] [--seconds 8] [--resolution 720p]
The key is read from .env and never printed. Polls until the video is ready, then downloads it.
"""
import argparse, base64, json, pathlib, sys, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://generativelanguage.googleapis.com/v1beta/"


def key():
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("GEMINI_API_KEY missing in .env")


def call(url, body=None):
    req = urllib.request.Request(url if url.startswith("http") else API + url,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"x-goog-api-key": key(), "Content-Type": "application/json"})
    try:
        return urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read()[:600].decode(errors='replace')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("prompt")
    ap.add_argument("--image"); ap.add_argument("--model", default="veo-3.1-lite-generate-preview")
    ap.add_argument("--aspect", default="16:9"); ap.add_argument("--seconds", type=int, default=8)
    ap.add_argument("--resolution", default="720p")
    a = ap.parse_args()
    inst = {"prompt": a.prompt}
    if a.image:
        img = pathlib.Path(a.image)
        inst["image"] = {"bytesBase64Encoded": base64.b64encode(img.read_bytes()).decode(),
                         "mimeType": "image/png" if img.suffix == ".png" else "image/jpeg"}
    body = {"instances": [inst], "parameters": {"aspectRatio": a.aspect, "durationSeconds": a.seconds, "resolution": a.resolution}}
    op = json.load(call(f"models/{a.model}:predictLongRunning", body))
    name = op["name"]
    print("started", name.split("/")[-1])
    while not op.get("done"):
        time.sleep(10)
        op = json.load(call(name))
    if "error" in op:
        sys.exit("failed: " + json.dumps(op["error"])[:600])
    resp = op["response"]
    samples = resp.get("generateVideoResponse", resp).get("generatedSamples") or resp.get("videos")
    uri = samples[0]["video"]["uri"]
    data = call(uri).read()
    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(data)
    print(out, len(data) // 1024, "KB")


if __name__ == "__main__":
    main()
