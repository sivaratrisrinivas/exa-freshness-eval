"""Build the hand-labeling queue: one row per unique (query, url) across all cached configs.
A human sets "relevant" to 1 if the page states the current answer for that query, else 0.
The answer-match hint is shown but is not the label."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from configs import CONFIGS
from checks import result_text, contains_current
from run import load_queries, cache_path, ROOT
qs = {q["id"]: q for q in load_queries()}; seen = set(); rows = []
for cfg in CONFIGS:
    for qid, q in qs.items():
        p = cache_path(cfg, qid)
        if not p.exists(): continue
        for r in (json.loads(p.read_text()).get("response") or {}).get("results") or []:
            if (qid, r["url"]) in seen: continue
            seen.add((qid, r["url"]))
            rows.append(dict(qid=qid, query=q["query"], answer=q["answer"], url=r["url"], title=r.get("title"),
                             published=r.get("publishedDate"), hint_match=contains_current(result_text(r), q), relevant=None))
out = ROOT / "data/labels_todo.jsonl"
out.write_text("".join(json.dumps(r) + "\n" for r in rows))
print(len(rows), "rows to label ->", out)
