import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
from checks import contains_current, contains_stale, grounded, stale, citation_precision, precision_at_k, result_text

Q = {"answer_patterns": [r"(?<![\d.])v?1\.4\.5(?![\d])"], "stale_answers": ["1.4.0"]}

def r(t, u="u"): return {"url": u, "title": "", "text": t}

def test_version_pass_and_borderlines():
    assert contains_current("released v1.4.5 today", Q)
    assert contains_current("langchain==1.4.5", Q)
    assert not contains_current("version 1.4.50", Q)      # longer version must not match
    assert not contains_current("version 11.4.5", Q)
    assert not contains_current("version 2.1.4.5", Q)

def test_stale_logic():
    assert stale([r("now 1.4.0")], Q) is True
    assert stale([r("now 1.4.0"), r("now 1.4.5")], Q) is False   # current present -> not stale
    assert stale([r("nothing")], Q) is False
    assert stale([r("x")], {"answer_patterns": ["x"], "stale_answers": []}) is None

def test_grounded_and_citation_precision():
    rs = [r("a"), r("v1.4.5"), r("b"), r("1.4.5")]
    assert grounded(rs, Q) and citation_precision(rs, Q) == 0.5
    assert not grounded([], Q) and citation_precision([], Q) == 0.0

def test_precision_at_k_counts_unlabeled():
    rs = [r("", "a"), r("", "b"), r("", "c")]
    p, unl = precision_at_k(rs, {"a": 1, "b": 0})
    assert p == 0.1 and unl == 1

def test_dash_normalisation():
    q = {"answer_patterns": [r"Antonelli.{0,60}340"], "stale_answers": []}
    assert contains_current(result_text({"title": "", "text": "Antonelli \u2014 340 pts"}), q)

def test_dataset_shape_and_frozen_heldout():
    import hashlib
    qs = [json.loads(l) for l in open(ROOT / "data/queries.jsonl")]
    assert len(qs) >= 50 and len({q["id"] for q in qs}) == len(qs)
    for q in qs:
        assert q["sources"] and q["changed_on"] >= "2026-09-14" and q["changed_on"] <= "2026-10-14"
    held = "".join(json.dumps(q, sort_keys=True) + "\n" for q in qs if q["split"] == "heldout")
    want = (ROOT / "data/FROZEN_HELDOUT.sha256").read_text().split()[0]
    assert hashlib.sha256(held.encode()).hexdigest() == want, "held-out split changed after freeze"

def test_replay_fixture_scores():
    qs = [json.loads(l) for l in open(ROOT / "data/queries.jsonl")]
    q = qs[0]
    rec = json.loads((ROOT / f"tests/fixtures/cache/auto/{q['id']}.json").read_text())
    res = rec["response"]["results"]
    assert grounded(res, q) and stale(res, q) is False and citation_precision(res, q) == 0.5
