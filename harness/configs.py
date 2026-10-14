"""Search configurations under test. Only parameters Exa ships; nothing is re-implemented."""
WINDOW_START = "2026-09-14T00:00:00.000Z"   # 30 days before the as-of date
AS_OF = "2026-10-14"
CONTENTS = {"text": {"maxCharacters": 4000}, "highlights": {"maxCharacters": 1000}}

def _c(**extra):
    c = dict(CONTENTS); c.update(extra); return c

CONFIGS = {
    # search types (current API enum: instant, fast, auto, deep-lite, deep, deep-reasoning)
    "instant":            {"type": "instant",   "contents": _c()},
    "fast":               {"type": "fast",      "contents": _c()},
    "auto":               {"type": "auto",      "contents": _c()},
    "deep-lite":          {"type": "deep-lite", "contents": _c()},
    "deep":               {"type": "deep",      "contents": _c()},
    # date / content-age settings, on auto and fast
    "auto+published30d":  {"type": "auto", "startPublishedDate": WINDOW_START, "contents": _c()},
    "fast+published30d":  {"type": "fast", "startPublishedDate": WINDOW_START, "contents": _c()},
    "auto+maxAge0":       {"type": "auto", "contents": _c(maxAgeHours=0)},
}
# Not run: "neural" and "keyword" are not in the current /search type enum (exa-spec.yaml, read 2026-10-14).
UNAVAILABLE = {"neural": "not in current type enum", "keyword": "not in current type enum",
               "deep-reasoning": "skipped for budget"}
