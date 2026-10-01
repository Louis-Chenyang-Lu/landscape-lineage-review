# Design Notes

## Why two phases

| | Breadth only | Depth only | Two phases |
|---|---|---|---|
| Output | A paper list grouped by theme | Causal chains for a few approaches | A map, plus causal explanations of its key routes |
| Main risk | Knowing *what* exists but not *why*, or what it means for your setting | Starting from the wrong anchor, or following one group's citations into a filter bubble | Slower; budgets are controlled by mode |

Phase 1 gives Phase 2 an **evidence-based starting point**: anchors are chosen from core papers, crowded themes and debates rather than intuition. Phase 2 in turn **explains the map**: debates between themes often exist because each side rests on different assumptions.

## Where the parts come from

**Phase 1 (breadth)** draws on the workflow publicly described by AI review tools such as Liner:
- expand the search vocabulary before searching
- retrieve widely, then filter
- select core papers and trace their citations
- organise by theme and highlight gaps
- evaluate progress and revisit earlier steps when needed

Changes made on top of that:
- The full search log is shown to the user.
- Core papers are selected on several signals, with citations adjusted for age so new work is not buried.
- Debates are identified explicitly and serve as the hand-off to Phase 2.
- Self-check conditions are stated precisely, with a cap on extra search rounds.

**Phase 2 (depth)** is principle-driven lineage analysis built on four questions: assumption, mechanism, price and regime. It adds:
- three retrieval channels: citation graph, limitation-driven queries and framing-driven queries
- cross-domain abstraction and transfer
- a coverage audit
- honest labelling of claims and reading depth

## Deliberate omissions

- **No paper-count targets.** Only work that changes an assumption or mechanism enters the lineage; incremental tuning gets one line at most.
- **No absolute "nobody has done this" claims.** Only "not found after searching A, B and C".
- **No built-in domain examples.** Templates use placeholders only, so one discipline's habits are not imposed on another.

## Portability

The skill follows the open [Agent Skills](https://agentskills.io) format: a folder with a `SKILL.md` (name + description frontmatter), optional `references/` and `scripts/`. It contains no agent-specific instructions, so the same folder works in Claude and Codex. `agents/openai.yaml` only adds display metadata for Codex / ChatGPT and is ignored elsewhere. The helper script uses only the Python standard library.
