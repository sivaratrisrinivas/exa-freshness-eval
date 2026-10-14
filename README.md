# Does Exa return the new answer after it changes?

Agents ask about things that changed last week. If search returns last month's version, price or CEO, the agent repeats it with confidence. Exa's Nitya Sridhar wrote that retrieval beyond model memory "requires specific focus on recency" (X, 29 Sep 2026), and Exa's WebCode post scores search on groundedness and citation precision. This repo applies that method to one question, as an independent test of features Exa already ships: **when the right answer changed in the last 30 days, does Exa return the new one?**

**Short answer: yes, almost always.** In every setting, the current answer appeared in the top 10 for 89 to 100% of queries. The current answer was the top result 74 to 100% of the time, and an old answer beat the new one in at most 2 of 15 held-out queries.

**[Live page](https://sivaratrisrinivas.github.io/exa-freshness-eval/)** · **[60s video](https://sivaratrisrinivas.github.io/exa-freshness-eval/exa-freshness-demo.mp4)**

## Setup
58 queries whose answer changed between 14 Sep and 14 Oct 2026, each with a dated answer and source links. They cover releases (30), prices (9), leadership changes (7), sports (6) and docs/API changes (6). The 19 held-out queries were picked by hash and frozen before any API call. Run on 14 Oct 2026, 361 calls, $2.44 reported by Exa.

## Results (dev 39 / held-out 19)
| config | top-1 has answer | top-10 has answer | citation precision | stale | P@10 | p50 latency |
|---|---|---|---|---|---|---|
| instant | .85 / .84 | .97 / 1.0 | .52 / .52 | 0 / 0 | .54 / .57 | 0.4 s |
| fast | .77 / .95 | 1.0 / 1.0 | .53 / .54 | 0 / 0 | .58 / .55 | 0.4 s |
| auto | .87 / .95 | 1.0 / 1.0 | .54 / .55 | 0 / .07 | .52 / .54 | 1.7 s |
| auto + published after 14 Sep | .74 / .74 | 1.0 / .89 | .60 / .63 | 0 / .13 | .60 / .74 | 1.6 s |
| fast + published after 14 Sep | .85 / .84 | 1.0 / .89 | .60 / .61 | 0 / .07 | .67 / .77 | 0.4 s |
| auto + maxAgeHours 0 | .90 / .95 | 1.0 / 1.0 | .62 / .60 | 0 / 0 | .54 / .56 | 9.6 s |
| deep-lite (15 queries) | 1.0 / 1.0 | 1.0 / 1.0 | .52 / .67 | 0 / 0 | n<3 | 3.1 s |

## What stood out
- The published-date filter makes results more precise (P@10 .74 to .77 on held-out), but it misses some fresh answers. About 65% of results carry no `publishedDate` (GitHub release pages, vendor docs), so the filter drops them. For releases a few hours old (uv 0.13.1, Terraform 1.16.6), only older third-party posts were left.
- `maxAgeHours: 0` gave the highest or tied-highest top-1 rate among the full runs and cost about 8 extra seconds per call.
- The one stale case without a date filter was an official help page dated April that still listed the old Disney+ price.

## Method notes
Every check is code (regex on result text), so there is no LLM judge. I hand-labeled 551 query and URL pairs (21 queries, all configs) for P@10. Against those labels the regex check had 22 false positives and 0 misses. `neural` and `keyword` are not in the current API, and `deep` was skipped for budget. Eval skills followed: `evals-start`, `write-code-eval`, and `error-discovery`. Error discovery was run as a solo review, not the interactive app (see `ERROR_ANALYSIS.md`). Limits: these are small samples, and both runs come from one day.

`python harness/score.py` rescores from `cache/` with no key, and CI does the same.
