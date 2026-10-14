# Error analysis (14 Oct 2026)

How it was done: I read every case where the current answer was missing from the top 10, or where an old answer showed up without the new one. I also read the title and the text around the match for all 551 hand-labeled query and URL pairs. This follows the error-discovery skill, but as a solo review. It did not use the interactive review app.

## Failure modes in the results
1. **Answer changed only hours before the run (filtered settings).** uv 0.13.1 (released 05:15 UTC on 14 Oct) and Terraform 1.16.6 (09:31 UTC on 14 Oct) appeared only on undated official pages. With `startPublishedDate`, those pages drop out, and third-party posts about 0.13.0 or 1.16.5 rank first. Held-out top-10 match fell from 1.0 to .89.
2. **Official page lags the change.** For "Disney+ with ads price", `auto` ranked help.disneyplus.com first. That page is dated 30 Apr and still shows $11.99, while news pages that rank lower show $12.49.
3. **Old release tag pages.** For release queries, many results are older GitHub tag pages, such as docker/compose v5.3.0 or vllm v0.24.0. They are on topic but don't give the latest version, so they pull P@10 down without making the answer stale.
4. **Undated results.** 63 to 68% of results in the unfiltered settings have no `publishedDate`, so date filtering removes most official sources.

## Failure modes in my own checker
Hand labels vs the regex check: 22 false positives and 0 false negatives. The causes were:
- The name appears but in an old role, such as "Jared Hyatt, Chief Financial Officer" or "Peter Anastasiou, COO".
- The number appears for a different item, such as Haiku 4.5's $0.10 cache price.
- Forks and mirror packages carry the same version number (@depup/supabase__supabase-js 2.117.3).
- The model name appears without the replacement relation (a page saying Opus 5.5 is available).

These inflate top-10 match, so top-1 match and hand-labeled P@10 are the more reliable columns.

## Dataset errata
I found these after freezing the split. I left them as recorded and did not edit them, to keep the hash.
- The Gemini 3.7 Flash and 3.5 Flash routing changes are dated 8 Oct in several sources. The dataset records 6 Oct, the date of the related changelog entry. The answers are unaffected.
- Some sports queries are easy, because a team name in the result text is enough to match. All configs score 1.0 on them.
