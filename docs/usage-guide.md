# Usage Guide

## 1. When to use it

**Good fit**
- Entering a new field and wanting to know its directions and how its focus has shifted
- Finding out what happened to a method, theory or study design after it was introduced, and why
- Writing a proposal or a related-work section that must explain how your work differs from prior work
- Suspecting your field's standard practice is outdated and checking whether other disciplines do better
- Looking for research gaps that are backed by evidence

**Poor fit**
- Systematic reviews that must follow PRISMA or similar protocols with fully reproducible search strings
- Finding one or two specific papers (a direct search is faster)

## 2. Writing a good prompt

The more specific you are, the better the result. Four kinds of information help most:

| Information | What to write |
|---|---|
| **Topic** | The object of study, the core question, or the method / theory you want to trace |
| **Your situation** | Data type, sample size, setting, disciplinary background |
| **What you care about** | What dissatisfies you about current practice, or the specific question you want answered |
| **Scope and depth** | Time window, whether to include preprints, quick or full review |

A broad topic on its own also works. The skill will pick the one or two most central sub-problems and tell you what it left out, but its choice may not match yours.

## 3. Choosing a mode

- **Quick**: the landscape only (core papers, themes, timeline, debates, preliminary gaps) plus suggested anchors to trace. Delivered in chat. Good for deciding where to dig.
- **Standard** (default): the landscape plus full lineage tracing for 1–3 anchors, cross-domain search, a coverage audit and a gap analysis.
- **Deep**: larger search budgets and more outside fields; best delivered as a document you can iterate on.
- **Trace**: for when you already have a seed paper or approach. Draws a small landscape around it, then traces its evolution.

A good rhythm: run Quick first, pick the anchors you actually care about, then run Trace or Standard on them.

## 4. Reading the results

1. **Search log.** Are the queries sensible? Is any common term from your field missing? If so, give it to the agent and re-run Phase 1.
2. **Coverage report.** Which channel returned nothing? Which fields were skipped? This determines how far to trust any "nobody has done X" statement.
3. **Landscape.** Are the works your advisor or peers consider important among the core papers? If not, the search vocabulary or scope is off.
4. **Lineage map and transitions.** Check everything labelled *inferred* first. These may be real insights or mistakes, and they are exactly where reading the original paper pays off.
5. **Transfer cards.** Entries marked "not found in the home field" are candidate contributions.
6. **References.** Prioritise reading key works marked "only seen cited".

## 5. Useful follow-ups

- "Add <paper / approach> as an anchor and re-run Phase 2."
- "Add <term> to the query set and redo Phase 1."
- "Use <discipline> as the outside field instead."
- "For the <A → B> transition, look for a fair comparison."
- "Map the open problems onto my project (<brief description>) and rank them."
- "Put the results into a document."

## 6. FAQ

**A reference cannot be found.**
The skill is instructed never to invent sources and to mark unverifiable ones as *unverified*. If an unmarked reference cannot be found, point it out and ask the agent to verify or remove it.

**The script prints `CHANNEL FAILED`.**
Usually a blocked network or a rate limit. Try `--backend openalex`, then fall back to web search. A failed channel means only that the channel failed, not that no related work exists. In Codex, check that network access is allowed.

**Does it work outside methodological fields?**
Yes. "Approach" covers methods, models, theories, frameworks, interventions, instruments and study designs; "assumption" includes theoretical premises, identification strategies, sampling frames and measurement validity.

**Which language does it answer in?**
The language of your question. Paper titles, approach names and technical terms stay in their original language so you can search for them.
