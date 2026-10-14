# Exa freshness eval

**Status: dataset, harness and CI are done. No Exa results yet: waiting on an API key.**

## Why
Agents ask about things that changed last week. A search result that shows last month's version, price or CEO is worse than no result, because the agent will repeat it with confidence. Exa's Nitya Sridhar wrote that retrieval beyond model memory "requires specific focus on recency", and that evals come from "manual dogfooding -> golden set of evals" (X, 29 Sep 2026). Exa's WebCode post (23 Mar 2026) scores search on groundedness and citation precision. This repo applies that same method to one narrow question: when the right answer changed in the last 30 days, does Exa return the new one?

This is an independent test of features Exa already ships (search types, `startPublishedDate`, `maxAgeHours`). It does not rebuild any of them.

## What is here
- `data/queries.jsonl`: 58 queries whose answer changed between 14 Sep and 14 Oct 2026. Each has the current answer, the old (stale) answer where one exists, the change date and source links. Categories: releases (30), prices (9), leadership (7), sports (6), docs/API changes (6).
- Held-out split: 19 queries, picked by hash, frozen in `data/FROZEN_HELDOUT.sha256` before any API call. CI fails if it changes.
- `harness/run.py`: runs every query against Exa `/search` for each config and caches the raw response in `cache/`.
- `harness/score.py`: scores cached responses. No key needed.
- `tests/`: unit tests for every check, plus a replay fixture. CI runs tests and scoring from cache only.

## Configs
| config | settings |
|---|---|
| instant, fast, auto, deep-lite, deep | `type` only |
| auto+published30d, fast+published30d | `startPublishedDate` = 2026-09-14 |
| auto+maxAge0 | `contents.maxAgeHours` = 0 (fresh fetch) |

`neural` and `keyword` are not in the current `/search` type enum, so they are not run. `deep-reasoning` is skipped to keep the budget small.

## Metrics (all code checks, no LLM judge)
- **Grounded**: any of the top 10 result texts contains the current answer (WebCode style, discriminative).
- **Citation precision**: share of the 10 results that contain the current answer.
- **Stale rate**: top 3 results show the old answer and none show the new one. Only for queries with a known old answer.
- **P@10**: against hand labels in `data/labels.jsonl` (queue built by `harness/label.py`).
- **Latency**: p50 and p90 wall clock per request.

## Results
_Pending. Will be split by dev and held-out._

## Eval skills followed
From `evals-skills`: `evals-start` (routing), `write-code-eval` (one code check per failure mode, tested on passes, fails and borderlines), `error-discovery` (to run on real traces once they exist). No LLM judge is used, so `write-judge-prompt` and `validate-evaluator` do not apply.

## Run it
```
EXA_API_KEY=... python harness/run.py --max-requests 470
python harness/score.py
```
