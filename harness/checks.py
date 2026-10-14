"""Code evaluators (write-code-eval). Objective rules only; no LLM judge."""
import re

def _norm(t):  # unify whitespace and unicode dashes so patterns match rendered pages
    return re.sub(r"\s+", " ", (t or "").replace("\u2013", "-").replace("\u2014", "-"))

def result_text(r):
    return _norm(" ".join([r.get("title") or "", r.get("text") or "", " ".join(r.get("highlights") or [])]))

def contains_current(text, q):
    return any(re.search(p, text, re.I) for p in q["answer_patterns"])

def contains_stale(text, q):
    for s in q.get("stale_answers") or []:
        s2 = s.lstrip("v")
        pat = r"(?<![\d.])v?" + re.escape(s2) + r"(?![\d])" if re.match(r"^v?\d", s) else re.escape(s)
        if re.search(pat, text, re.I):
            return True
    return False

def grounded(results, q, k=10):
    """WebCode-style groundedness: does any of the top-k result texts contain the current answer?"""
    return any(contains_current(result_text(r), q) for r in results[:k])

def citation_precision(results, q, k=10):
    """WebCode-style: share of returned results (top-k) whose text contains the current answer."""
    rs = results[:k]
    return sum(contains_current(result_text(r), q) for r in rs) / len(rs) if rs else 0.0

def stale(results, q, k=3):
    """Stale answer: top-k texts show a pre-change answer and none shows the current one.
    Only defined for queries that have a known stale answer."""
    if not q.get("stale_answers"):
        return None
    texts = [result_text(r) for r in results[:k]]
    return any(contains_stale(t, q) for t in texts) and not any(contains_current(t, q) for t in texts)

def precision_at_k(results, labels, k=10):
    """labels: {url: 0/1} hand labels for this query. Unlabeled URLs count as not relevant
    and are reported separately so coverage is visible."""
    rs = results[:k]
    if not rs:
        return 0.0, 0
    rel = sum(labels.get(r["url"], 0) for r in rs)
    unlabeled = sum(r["url"] not in labels for r in rs)
    return rel / k, unlabeled
