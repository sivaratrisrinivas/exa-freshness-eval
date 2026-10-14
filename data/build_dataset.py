"""Builds data/queries.jsonl from verified facts. Run once; output is frozen by hash."""
import json, re, hashlib
rel = json.load(open("data/releases_raw.json"))
Q = []
def add(cat, q, ans, aliases, stale, changed, sources, note=""):
    Q.append(dict(category=cat, query=q, answer=ans, answer_patterns=aliases, stale_answers=stale,
                  changed_on=changed, sources=sources, note=note))
def vpat(v):
    v = v.lstrip("v"); return [r"(?<![\d.])v?" + re.escape(v) + r"(?![\d])"]
for r in rel:
    add("releases", f"latest stable release of {r['name']}", r["cur"].lstrip("v"), vpat(r["cur"]),
        [r["prev"].lstrip("v")] if r["prev"] else [], r["date"][:10], [r["url"]],
        f"GitHub release published {r['date']}; previous stable before 2026-09-14 was {r['prev']}")
P="prices"
add(P,"Disney+ Premium no ads monthly price US","$21.49",[r"21\.49"],["$18.99"],"2026-09-23",["https://www.macrumors.com/2026/09/23/disney-plus-hulu-price-increase/","https://variety.com/2026/tv/news/disney-plus-hulu-price-increase-2026-1236873281/"])
add(P,"Disney+ with ads monthly price US","$12.49",[r"12\.49"],["$11.99"],"2026-09-23",["https://www.macrumors.com/2026/09/23/disney-plus-hulu-price-increase/"])
add(P,"Hulu no ads monthly price","$21.49",[r"21\.49"],["$18.99"],"2026-09-23",["https://www.macrumors.com/2026/09/23/disney-plus-hulu-price-increase/"])
add(P,"Disney+ Hulu Premium bundle no ads price per month","$21.99",[r"21\.99"],["$19.99"],"2026-09-23",["https://variety.com/2026/tv/news/disney-plus-hulu-price-increase-2026-1236873281/"])
add(P,"ESPN Unlimited streaming monthly price","$31.99",[r"31\.99"],["$29.99","$30"],"2026-09-17",["https://forbesamerica.com/espn-hikes-streaming-prices-september-2026/","https://variety.com/2026/tv/news/disney-plus-hulu-price-increase-2026-1236873281/"])
add(P,"ESPN Select monthly price","$13.99",[r"13\.99"],["$13","$12.99"],"2026-09-17",["https://forbesamerica.com/espn-hikes-streaming-prices-september-2026/"])
add(P,"Claude Haiku 5.5 API price per million input and output tokens","$0.10 / $0.50",[r"\$?0?\.10\b.{0,40}\$?0?\.50\b"],["$1 / $5"],"2026-10-07",["https://aitokenprice.com/reports/2026-10"])
add(P,"Claude Sonnet 5.5 cache read price per million tokens","$0.10",[r"\$0?\.10"],["$0.20"],"2026-10-07",["https://aitokenprice.com/reports/2026-10"])
add(P,"cheapest gpt-oss-120b price on OpenRouter per million tokens","$0.03 / $0.15",[r"\$?0?\.03\d?\b.{0,40}0?\.15\b"],["$0.15 / $0.60"],"2026-10-13",["https://aitokenprice.com/reports/2026-10"])
L="leadership"
add(L,"Globality CEO","Jared Hyatt",[r"Jared Hyatt"],["Joel Hyatt"],"2026-10-14",["https://procurementmag.com/news/jared-hyatt-named-new-globality-ceo-as-joel-hyatt-steps-down"])
add(L,"Wrist Group new Group CEO","Robert Desai",[r"Robert Desai"],["Jens Holger Nielsen"],"2026-10-14",["https://www.wrist.com/news-expos/post/wrist-group-appoints-robert-desai-as-group-ceo"])
add(L,"Harmony Biosciences next CEO","Peter Anastasiou",[r"Anastasiou"],["Jeffrey Dayno"],"2026-10-12",["https://www.stocktitan.net/sec-filings/HRMY/8-k-harmony-biosciences-holdings-inc-reports-material-event-0865da5b68ed.html"])
add(L,"AngioDynamics new CEO","Eric Honroth",[r"Honroth"],["Jim Clemmer"],"2026-10-08",["https://www.sec.gov/Archives/edgar/data/1275187/000114036126039019/ef20083270_ex99-1.htm"])
add(L,"Adeia CEO","Dipti Vachani",[r"Vachani"],["Paul E. Davis","Paul Davis"],"2026-09-28",["https://adeia.com/press-release/adeia-appoints-dipti-vachani-as-chief-executive-officer"])
add(L,"Similarweb new CEO","Michael Akkerman",[r"Akkerman"],["Or Offer"],"2026-09-24",["https://www.nasdaq.com/press-release/similarweb-names-michael-akkerman-new-chief-executive-officer-2026-09-24"])
add(L,"Percheron Therapeutics CEO","Michael Baker",[r"Michael Baker"],["James Garner"],"2026-10-05",["https://app.dealroom.co/news/feed/percheron-therapeutics-appoints-michael-baker-as-ceo-ahead-of-hmbd-002-trial-in-h2-2026"])
S="sports"
add(S,"who won the 2026 ALDS Rays vs Yankees","Tampa Bay Rays (3-0)",[r"Rays"],[],"2026-10-07",["https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule"])
add(S,"2026 ALDS Guardians vs White Sox result","Cleveland Guardians won 3-2",[r"Guardians"],[],"2026-10-10",["https://www.baseball-reference.com/postseason/2026_ALDS2.shtml"])
add(S,"2026 NLDS Dodgers vs Braves winner","Los Angeles Dodgers 3-1",[r"Dodgers"],[],"2026-10-07",["https://www.mlb.com/news/dodgers-win-nlds-2026"])
add(S,"2026 NLDS Brewers vs Padres winner","Milwaukee Brewers 3-1",[r"Brewers"],[],"2026-10-07",["https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule"])
add(S,"F1 2026 drivers championship leader points","Kimi Antonelli, 340 points",[r"Antonelli.{0,60}340|340.{0,60}Antonelli"],[],"2026-10-11",["https://www.formula1.com/en/results/2026/drivers","https://www.motorsportweek.com/2026/10/13/f1-2026-drivers-championship-after-singapore-gp/"])
add(S,"2026 Singapore Grand Prix winner","Max Verstappen",[r"Verstappen"],[],"2026-10-11",["https://www.formula1.com/en/results/2026/races/1296/singapore/race-result"])
D="docs_api"
add(D,"gemini-3.7-flash deprecated replacement model","gemini-3.8-flash",[r"3\.8[- ]flash"],[],"2026-10-06",["https://ai.google.dev/gemini-api/docs/changelog","https://releases.fru.dev/releases/gemini-api-2026-10-06-deprecation-announcement"])
add(D,"gemini-3.5-flash requests routed to which model","gemini-3.6-flash",[r"3\.6[- ]flash"],[],"2026-10-06",["https://ai.google.dev/gemini-api/docs/changelog"])
add(D,"gemini-3.1-flash-image deprecated migrate to","gemini-nano-banana-2.1",[r"nano[- ]banana[- ]2\.1"],[],"2026-10-06",["https://releases.fru.dev/releases/gemini-api-2026-10-06-deprecation-announcement"])
add(D,"GitHub Copilot Claude Opus 4.7 deprecated suggested alternative","Claude Opus 5.5",[r"Opus 5\.5"],["Claude Opus 5"],"2026-10-02",["https://github.blog/changelog/2026-10-02-selected-models-in-github-copilot-deprecated/"],"Sep 3 notice said Opus 5; Oct 2 changelog says Opus 5.5")
add(D,"OpenAI GPT-4o API shutdown date and recommended replacement","January 14, 2027; gpt-6-luna",[r"gpt-6-luna|January 14, 2027"],[],"2026-10-14",["https://developers.openai.com/api/docs/deprecations"])
add(D,"Gemini deep-research-pro-preview-12-2025 shutdown date","October 23, 2026",[r"October 23, 2026|2026-10-23"],[],"2026-10-06",["https://ai.google.dev/gemini-api/docs/changelog"])
for q in Q:
    q["id"] = hashlib.sha1(q["query"].encode()).hexdigest()[:8]
    # held-out: deterministic hash split (~30%), independent of any results
    q["split"] = "heldout" if int(hashlib.sha256(("exa-fresh-v1"+q["id"]).encode()).hexdigest(),16) % 10 < 3 else "dev"
with open("data/queries.jsonl","w") as f:
    for q in Q: f.write(json.dumps(q)+"\n")
from collections import Counter
print(len(Q), Counter(q["category"] for q in Q), Counter(q["split"] for q in Q))
