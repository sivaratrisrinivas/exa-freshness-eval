"""Run queries x configs against Exa /search, caching every raw response.
Replay mode (no key) reads only from cache/. Usage:
  python harness/run.py [--replay] [--configs a,b] [--max-requests N]
"""
import argparse, hashlib, json, os, sys, time, pathlib
import urllib.request, urllib.error
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from configs import CONFIGS, SAMPLE_ONLY
ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"

def load_queries():
    return [json.loads(l) for l in open(ROOT / "data/queries.jsonl")]

def cache_path(cfg, qid):
    return CACHE / cfg / f"{qid}.json"

def call_exa(body, key):
    req = urllib.request.Request("https://api.exa.ai/search", data=json.dumps(body).encode(),
                                 headers={"x-api-key": key, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read()); status = r.status
    except urllib.error.HTTPError as e:
        data = {"error": e.read().decode()[:2000]}; status = e.code
    return {"status": status, "latency_s": round(time.time() - t0, 3), "request": body, "response": data,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}

def cost_of(rec):
    c = (rec.get("response") or {}).get("costDollars") or {}
    return float(c.get("total") or 0)

def spent_so_far():
    return sum(cost_of(json.loads(p.read_text())) for p in CACHE.glob("*/*.json"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", action="store_true")
    ap.add_argument("--configs", default=",".join(CONFIGS))
    ap.add_argument("--max-requests", type=int, default=int(os.environ.get("EXA_MAX_REQUESTS", 470)))
    a = ap.parse_args()
    key = os.environ.get("EXA_API_KEY")
    if not a.replay and not key:
        sys.exit("EXA_API_KEY not set; use --replay to score cached responses")
    qs = load_queries(); used = 0; missing = 0
    cap = float(os.environ.get("EXA_SPEND_CAP", 4.9)); spent = spent_so_far()
    for cfg in a.configs.split(","):
        for q in (qs[:SAMPLE_ONLY[cfg]] if cfg in SAMPLE_ONLY else qs):
            p = cache_path(cfg, q["id"])
            if p.exists():
                continue
            if a.replay:
                missing += 1; continue
            if spent >= cap:
                print(f"spend cap reached: ${spent:.3f}"); return
            if used >= a.max_requests:
                print("request budget reached", used); return
            body = dict(CONFIGS[cfg]); body["query"] = q["query"]; body["numResults"] = 10
            rec = call_exa(body, key); used += 1
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(rec, indent=1))
            spent += cost_of(rec)
            print(cfg, q["id"], rec["status"], rec["latency_s"], f"total=${spent:.3f}")
            if rec["status"] == 429: time.sleep(5)
    print(f"done; live requests={used}; missing in replay={missing}")

if __name__ == "__main__":
    main()
