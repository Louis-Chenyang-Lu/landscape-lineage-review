---
name: landscape-lineage-review
description: Two-phase literature review for any research field. Phase 1 (Landscape) maps the field broadly - expands search vocabulary, retrieves widely, selects core papers, clusters themes and shows how the focus shifted over time. Phase 2 (Lineage) takes anchor approaches from that map and traces how each evolved - which assumption it makes, which limitation that causes, which later work relaxed it and at what price - including better versions developed in other fields. Ends with a frontier and gap synthesis, a coverage audit and verified references. Use this skill whenever the user asks for a literature review, 文献综述, 调研, related work, state of the art, a field overview, research gaps, citation chasing, 顺藤摸瓜, how a method or theory evolved, or whether something in their field was improved elsewhere, including quick overviews, even if they don't say "literature review".
---

# Landscape → Lineage Literature Review

Two questions make a literature review useful, and they need different methods:

- **Where is everything?** (breadth) — which work exists, how it clusters into themes, how the focus has moved over time. Answered by wide, transparent retrieval. → **Phase 1: Landscape**
- **Why is it this way, and what comes next?** (depth) — why each approach replaced its predecessor, when each still wins, and which problems nobody has solved. Answered by tracing causal chains of assumptions. → **Phase 2: Lineage**

Phase 1 decides *what* to trace; Phase 2 explains it. A reader should finish the review able to find their way around the field **and** predict when each approach will succeed or fail.

Respond in the user's language. Keep paper titles, approach names and technical terms in their original language so the user can search for them.

**Terminology.** "Approach" means whatever the field's units of progress are: a method, model, algorithm, theory, framework, intervention, instrument, or study design. "Assumption" includes mathematical assumptions, theoretical premises, identification strategies, sampling frames, measurement validity, and implicit conditions about the setting. The workflow is the same for quantitative and qualitative fields.

## Choose a mode

| Mode | When | What runs |
|---|---|---|
| **Quick** | User wants an overview, says "quick/brief/先扫一遍", or is new to the field | Phase 0–1, short audit; answer in chat |
| **Standard** (default) | General request for a review | All phases; 1–3 anchors; 3–4 hops; ~15–30 core papers total |
| **Deep** | User says thorough / exhaustive / for a thesis or paper | All phases with larger budgets and more outside fields; deliver as a document |
| **Trace** | User names a seed paper or approach and asks how it evolved | Light Phase 1 around the seed (one retrieval round), then Phase 2 |

State the mode you chose in one line. If the request is ambiguous only about mode, pick one and proceed rather than asking.

## The core rule: principles, not facts

Every comparison between approaches is stated as a mechanism, not a result.

- ❌ Fact: "B outperforms A by N% on benchmark X."
- ✅ Principle: "A assumes property P of the data or setting. When P fails, A is biased or breaks in a specific way. B removes the need for P through mechanism M, at the price of cost C. So B should win when P is clearly violated, while A stays preferable when P roughly holds or C is unaffordable. B's reported gain on X supports this only if X actually violates P."

A usable principle statement answers four questions:
1. **Assumption changed** — what did the older approach assume (explicitly or implicitly) that the newer one drops, relaxes or replaces?
2. **Mechanism** — which concrete design choice makes that possible?
3. **Price** — what new assumption, cost, data requirement or failure mode does the newer approach bring? There is almost always one; look harder before claiming there is none.
4. **Regime** — under which conditions should the newer approach win, and when is the older one still the better choice?

Numbers may serve as *evidence for* a principle, never as a replacement for one. A claimed gain with no identifiable mechanism is itself a finding; report it as such.

## Tools for retrieval

Use what is available, in this order, and record which you used:
1. Scholarly search connectors or tools present in the session (academic search, citation databases).
2. `scripts/scholar_tool.py` (Semantic Scholar / OpenAlex): `landscape` for multi-query retrieval with deduplication, `forward` / `backward` for citation chaining, `search` for single lookups. Run `python scripts/scholar_tool.py -h` for usage.
3. General web search, with queries aimed at scholarly sources (preprint servers, publisher pages, institutional repositories).

If a tool fails (blocked network, rate limit), fall back to the next one and record the failure. A failed channel never means "nothing exists".

## Phase 0 — Frame the problem

Briefly, by yourself:
- **Task definition**: the object of study, the research question(s), and (for methodological topics) inputs, outputs and objective.
- **Design axes**: the main dimensions along which approaches differ. These become the vocabulary for every later comparison.
- **Task framings**: the different problem types under which the same object is studied (for example description, prediction, causal inference, measurement, intervention, generation, integration with other data). Improvements are often published under a framing different from the anchor's, so every framing gets searched.
- **Scope**: time window, which literatures count (peer-reviewed, preprints, grey literature, books), languages.

If the topic contains several unrelated sub-problems, choose the 1–2 most central to the user's stated interest and say what you left out. Ask a clarifying question only if the topic is genuinely ambiguous; otherwise state the framing and proceed.

## Phase 1 — Landscape (breadth)

### 1.1 Expand the search vocabulary
Build a **query set** before searching. Cover:
- core terms and their synonyms, abbreviations and alternative spellings;
- broader and narrower terms;
- the terms adjacent fields use for the same concept;
- one query per task framing from Phase 0;
- a survey/review query, a recency query (last 12–18 months), and a query aimed at the field's high-visibility venues.

Write the query set into a **search log** (template in `references/templates.md`). The log is shown to the user: it lets them check the search and reuse the terms themselves.

### 1.2 Retrieve and filter
Run every query. Deduplicate (same DOI / arXiv id / title). Filter against explicit inclusion criteria derived from Phase 0, and write the criteria down. Record counts: retrieved → after deduplication → kept.

### 1.3 Select core papers
Rank candidates using several signals together, never one alone:
- found by several different queries;
- citations **relative to age** (recent work cannot have many citations yet; do not penalise it);
- cited by surveys, or used as a baseline by other papers;
- venue and evidence quality;
- direct relevance to the framed task.

Keep about 8–20 core papers (fewer in Quick mode). For each, note in one line *why* it is core. Use the core-paper table in `references/templates.md`.

### 1.4 Snowball one hop
For each core paper, look one step backward (what it cites) and forward (what cites it). Add papers that are relevant and missing; do not chain further here — deep chaining is Phase 2's job.

### 1.5 Map themes, timeline and debates
- Cluster the kept papers into 3–7 **themes** by the question or approach they share. Describe each theme in 2–3 sentences and list its core papers.
- Draw a **timeline** of how the field's focus shifted (which themes rose, merged or faded, and roughly when).
- Identify **debates**: places where findings or positions disagree. For each, give the most plausible reason for the disagreement (different assumptions, data, settings, measures) — this is where Phase 2 often starts.

### 1.6 Self-check, then iterate if needed
Before moving on, check:
- Does every task framing have at least one theme or an explicit "nothing found"?
- Is any theme supported by only one paper or one research group?
- Are the last 12–18 months represented?
- Did any query return mostly noise (a sign the vocabulary is off)?

If a check fails, return to 1.1 with new queries. At most two extra rounds; report what still fails.

### 1.7 Choose anchors for Phase 2
Pick **1–3 anchor approaches** the landscape shows to be reference points. Name the sense of "state of the art" used (best performance, most adopted, or conceptual standard) and justify each choice in one line. Prefer anchors that sit at the centre of a debate or a heavily populated theme.

For each anchor record its **aliases**: full title, approach name, every acronym or alternative name others use for it, first author and year, DOI/arXiv id. Later work often cites an approach under a name its authors never used; every search in Phase 2 runs over all aliases.

**Quick mode stops here**: deliver the landscape, preliminary gaps (labelled as preliminary), and the suggested anchors with one line each on what a lineage trace would clarify.

## Phase 2 — Lineage (depth)

### 2.1 Principle card for each anchor
Fill the principle card in `references/templates.md`. The most important fields are the core assumptions (including implicit ones), the mechanism, and the **limitations derived from the assumptions**, kept separate as:
- limitations the authors admit;
- limitations reported by later work;
- limitations you infer from the assumptions (mark them as inferred).

### 2.2 Chain forward through three channels
For each node, find successors through three independent channels. Each catches work the others miss, so run all three.

1. **Citation graph** — who cites the node or compares against it. Papers that use the node **only as a baseline** count; they rarely say they fix its limitation, yet they are often the strongest successors. Use `scholar_tool.py forward`, or search every alias with phrases like "compared with", "baseline", "outperforms", "extends".
2. **Limitation-driven** — turn each limitation on the card into a query that describes a *fix* in generic words, without naming the node. This finds successors that never cite it.
3. **Framing-driven** — for each task framing, search the object of study plus that framing, including a recency query and a high-visibility-venue query.

Also look sideways (concurrent work fixing the same limitation differently — two different fixes reveal what the problem really is) and, if the anchor itself is unclear, briefly backward.

Keep a successor only if it changes an **assumption or mechanism** relevant to a limitation on the card. Incremental work (more data, a new backbone, tuning, a new application of the same idea) gets one line at most.

For each kept successor, write its principle card and a **transition statement** (old → new) answering the four questions of the core rule.

### 2.3 Escape the home field
Run this whenever the topic sits in a focused application field, and always when the home-field chain looks stale (anchor several years old, successors only applications or tuning, limitations acknowledged but unfixed). A field's standard approach may never have been improved inside that field while the same underlying approach has been criticised and improved elsewhere.

1. **Abstract the approach.** Rewrite each key approach as a domain-free problem: the object, the model or argument, the estimator or procedure, the assumptions. Remove all domain vocabulary. List the names this abstract problem goes by in other fields.
2. **Find where its limitations were diagnosed.** A limitation is often first identified in another community. Search the abstract formulation together with the limitation, and forward-chain the *generic* ancestor of the approach, not only the home-field paper.
3. **Chain to the outside frontier** using 2.2 and 2.4. Write principle cards and transition statements there too, recording each node's field.
4. **Check the outside frontier's own open limitations** — these, not the home-field ones, are the truly unsolved problems.
5. **Transfer back.** For each promising outside approach, fill a transfer card (`references/templates.md`): do the home field's data and settings satisfy its assumptions; what adaptation is needed and what could break; has anyone already applied it in the home field (search specifically — if yes, it becomes a home-field node; if no, it is a candidate contribution); what gain to expect and in which regime.

Budget: 1–3 outside fields, chosen by how close their formulation is to the abstracted problem. Say which fields you checked and which you skipped.

### 2.4 Iterate to the frontier
Repeat 2.2 on new nodes. Standard budget: 3–4 hops, 2–4 successors per node. Stop a branch when the newest node is within about 12 months and has no substantive follow-ups yet, or when successors stop changing assumptions (the branch has matured into engineering or routine application).

Track branches that **merge** (later work combines two fixes) and limitations that **reappear** (a fix that reintroduces an earlier problem). Both are high-value observations.

### 2.5 Connect lineage back to the landscape
Place every lineage node on the theme map. Note which debates from 1.5 the lineage explains (two sides of a debate often rest on different assumptions), and which themes the lineage did not touch.

## Phase 3 — Coverage audit (before writing)

Check and report each item. Fix gaps by searching, not by adding caveats.
- Every query in the search log was run; counts recorded.
- Every alias of every anchor was searched for citing and baseline relations.
- Every limitation on every card has at least one fix-query.
- Every task framing was searched, including the recency and high-visibility-venue queries.
- **Source diversity**: if more than about half of the nodes or core papers come from one group or co-author network, search deliberately outside it. Following one group's reference lists reproduces that group's view of the field.
- **Channel yield**: note which channel or tool found each node. A channel with zero yield more likely failed than proved absence.

Claims such as "nobody has done X" are only as strong as this audit; write them as "not found after searching A, B and C".

## Phase 4 — Frontier and gaps

Distinguish two kinds of gap:
- **Landscape gaps** (from Phase 1): under-studied questions, populations, settings, data types or time periods; themes with thin or contradictory evidence.
- **Mechanistic gaps** (from Phase 2): assumptions that *every* current frontier approach still makes; tensions where fixing one problem always costs another; improvements that exist in an outside field but have not been transferred.

Then:
- Compare the home-field frontier with the cross-domain frontier: how far behind is the home field, and which improvements are ready to transfer?
- Rank opportunities: (a) transfer an outside approach whose assumptions fit; (b) fix an open limitation of the outside frontier and apply it at home; (c) fill a landscape gap. Give the main risk of each and say why the hard ones are hard.
- If the user described their own project, connect the ranked opportunities to it.

## Output format

Deliver in this order, adapting headings to the user's language:

1. **Framing and scope** — task definition, design axes, framings, scope, mode chosen, domain-free formulation (short).
2. **Search log** — queries, tools used, counts (retrieved → deduplicated → kept), inclusion criteria.
3. **Landscape** — core-paper table, themes, timeline, debates.
4. **Lineage map** — a Mermaid graph: nodes = approaches (name, year); edges labelled with the assumption relaxed; anchors and frontier nodes marked; nodes grouped by field in subgraphs, with cross-field edges.
5. **Transitions** — one short section per edge with the four-question statement and its evidence.
6. **Comparison table** — approaches × design axes, plus "wins when" and "fails when" columns describing regimes, not scores.
7. **Cross-domain transfer** — abstract formulation, fields searched, a transfer card per candidate.
8. **Frontier and gaps** — Phase 4, with shared unresolved assumptions highlighted and opportunities ranked.
9. **Coverage** — the Phase 3 audit, including what was not covered.
10. **References** — every work with year, venue or preprint id, and a link; mark each as read in full, read as abstract, or only seen cited.

Quick mode delivers 1–3, preliminary gaps and suggested anchors. For Standard and Deep reviews, put the result in a document or file if the user wants something to keep.

## Honesty rules

- Never invent a paper, author, year, venue or result. If a work cannot be verified, drop it or mark it "unverified".
- Label claims as **claimed** (the authors say so), **demonstrated** (shown by a fair comparison) or **inferred** (your reasoning).
- Point out unfair comparisons (different data, compute, tuning effort, populations) and limit conclusions accordingly.
- Citation chaining creates filter bubbles; the limitation-driven and framing-driven channels exist to break them. Never skip them because the citation channel looked productive.
- Say what you did not cover. The review is a map for the user to verify and read from, not a substitute for reading the key sources.
