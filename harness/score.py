"""Score cached responses. Writes results/summary.json and results/summary.md, split by dev / heldout."""
import json, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from configs import CONFIGS
from checks import grounded, citation_precision, stale, precision_at_k
from run import load_queries, cache_path, ROOT

def load_labels():
    p = ROOT / "data/labels.jsonl"; L = {}
    if p.exists():
        for l in open(p):
            r = json.loads(l); L.setdefault(r["qid"], {})[r["url"]] = int(r["relevant"])
    return L

def main(splits=("dev", "heldout")):
    qs = load_queries(); labels = load_labels(); out = {}
    for cfg in CONFIGS:
        for sp in splits:
            rows = []
            for q in [q for q in qs if q["split"] == sp]:
                p = cache_path(cfg, q["id"])
                if not p.exists(): continue
                rec = json.loads(p.read_text())
                res = (rec.get("response") or {}).get("results") or []
                ok = rec["status"] == 200
                s = stale(res, q)
                pk, unl = precision_at_k(res, labels.get(q["id"], {})) if q["id"] in labels else (None, None)
                rows.append(dict(qid=q["id"], cat=q["category"], ok=ok, grounded=grounded(res, q),
                                 cite_prec=citation_precision(res, q), stale=s, p10=pk, latency=rec["latency_s"]))
            if not rows: continue
            m = lambda xs: round(statistics.mean(xs), 3) if xs else None
            st = [r["stale"] for r in rows if r["stale"] is not None]
            p10 = [r["p10"] for r in rows if r["p10"] is not None]
            lat = sorted(r["latency"] for r in rows if r["ok"])
            out[f"{cfg}|{sp}"] = dict(config=cfg, split=sp, n=len(rows), errors=sum(not r["ok"] for r in rows),
                grounded=m([r["grounded"] for r in rows]), citation_precision=m([r["cite_prec"] for r in rows]),
                stale_rate=m(st), stale_n=len(st), p_at_10=m(p10), p10_n=len(p10),
                latency_p50=lat[len(lat)//2] if lat else None, latency_p90=lat[int(len(lat)*.9)] if lat else None,
                by_category={c: m([r["grounded"] for r in rows if r["cat"] == c]) for c in sorted({r["cat"] for r in rows})},
                rows=rows)
    (ROOT / "results").mkdir(exist_ok=True)
    json.dump(out, open(ROOT / "results/summary.json", "w"), indent=1)
    lines = ["| config | split | n | grounded | citation prec | stale rate | P@10 | p50 s | p90 s | errors |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in out.items():
        lines.append(f"| {v['config']} | {v['split']} | {v['n']} | {v['grounded']} | {v['citation_precision']} | {v['stale_rate']} (n={v['stale_n']}) | {v['p_at_10']} (n={v['p10_n']}) | {v['latency_p50']} | {v['latency_p90']} | {v['errors']} |")
    (ROOT / "results/summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
