# Templates

Keep each field short (1–3 sentences). Prefer mechanisms over numbers. Placeholders are in `<angle brackets>`.

## Search log (Phase 1.1–1.2)

```
Mode: <Quick | Standard | Deep | Trace>
Tools used: <connector / scholar_tool.py backend / web search>; failures: <tool: reason>
Inclusion criteria: <what counts as relevant>  Exclusion: <what was dropped and why>

| # | Query | Purpose (synonym / framing / recency / survey / venue / adjacent field) | Hits | Kept |
|---|-------|----------------------------------------------------------------------|------|------|

Totals: retrieved <n> → after deduplication <n> → kept <n>
Self-check rounds: <n>; checks still failing: <...>
```

## Core-paper table (Phase 1.3)

```
| Paper (first author, year) | Venue / id | Theme | Why core (signals) | Read level |
|----------------------------|------------|-------|--------------------|------------|
```
Signals: multi-query hit, citations relative to age, cited by surveys, used as baseline, venue, direct relevance.

## Theme card (Phase 1.5)

```
### Theme: <short name>
Shared question / approach: <...>
Core papers: <...>
Period of activity: <when it rose / peaked / faded>
Internal debate: <position A vs position B; likely reason they differ>
Evidence strength: <many groups / one group / thin / contradictory>
```

## Principle card (Phase 2.1)

```
### <Approach name> (<first author>, <year>, <venue / preprint id>)
Field:                    <home field | outside field>
Problem it targets:       <which limitation of which predecessor, or which gap>
Core assumptions:         <explicit> ; implicit: <relied on but not stated>
Mechanism:                <the key design choice, in one sentence>
Why it works (principle): <causal link from mechanism to gain>
Price paid:               <new assumptions, cost, data needs, parameters, failure modes>
Wins when:                <regime>
Fails / degrades when:    <regime>
Limitations:
  - [author-stated]       <...>
  - [reported by <work>]  <...>
  - [inferred]            <...> (derived from assumption <...>)
Evidence quality:         <fair comparison? ablation isolating the mechanism? which evaluations?>
Successors to check:      <from citing work / limitation queries / framing queries>
Read level:               full text | abstract | only seen cited
```

## Transition statement (Phase 2.2)

```
<Old approach> → <New approach>
Assumption changed: <...>
Mechanism:          <...>
Price:              <...>
Regime:             new wins when <...>; old still preferable when <...>
Evidence:           claimed / demonstrated / inferred — <brief justification>
Found via:          citation graph | limitation-driven | framing-driven | sideways
```

## Transfer card (Phase 2.3)

```
<Outside approach> (<field>) → <home-field problem>
Shared abstract problem:  <domain-free formulation both fit>
Assumptions it needs, and whether the home field satisfies them:
  - <assumption>: holds / violated because <...> / unknown
Adaptation needed:        <...>
Risks:                    <what could break on home-field data or settings>
Already used at home?     yes (<cite>) / not found after searching "<queries>"
Expected gain and regime: <which question it answers better, and when>
Open limitation to target:<limitation of the outside frontier worth fixing>
```
