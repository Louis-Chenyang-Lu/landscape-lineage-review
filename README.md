# Landscape → Lineage Review

**Map the field first, then trace how its ideas evolved.**
An agent skill for literature reviews in any research field, compatible with **Claude** (Claude.ai, desktop, Claude Code) and **OpenAI Codex** (CLI, IDE extension, ChatGPT desktop app).

> **中文简介：** 一个适用于任何研究领域的文献综述 Skill，支持 Claude 和 Codex。先画出领域全景，再顺藤摸瓜追踪关键方法的演进。详见下方 [中文摘要](#中文摘要)。

---

## Why this skill

A useful literature review answers two different questions, and each needs a different method:

| | Question | What it takes |
|---|---|---|
| **Breadth** | What exists? How does it cluster? How has the focus shifted? Where do findings disagree? | Wide, transparent retrieval and organisation |
| **Depth** | Why did later approaches replace earlier ones? When does each still win? What remains unsolved? | Tracing causal chains of assumptions, limitations, fixes and trade-offs |

Most AI review tools excel at breadth: they retrieve many papers, group them by theme and draft a cited summary. Breadth alone, however, yields a list of who did what, without explaining *why* or *what it means for your setting*. Depth alone risks starting the trace from the wrong place.

This skill chains the two into one pipeline: **the landscape decides what to trace, and the lineage explains the landscape.**

## How it works

```
Phase 0  Framing        Task definition · design axes · task framings · scope
   │
Phase 1  Landscape      Expand search vocabulary → retrieve & deduplicate → select core papers
  (breadth)             → one-hop snowballing → themes / timeline / debates
                        → self-check and re-search if thin → choose anchors
   │
Phase 2  Lineage        Principle cards → three-channel forward chaining
  (depth)               → escape the home field (cross-domain transfer)
                        → iterate to the frontier → place lineage back on the map
   │
Phase 3  Coverage       Queries · aliases · every limitation · every framing
         audit          · source diversity · per-channel yield
   │
Phase 4  Frontier       Landscape gaps + mechanistic gaps, ranked by value and risk
         & gaps
```

## Key features

- **Principles, not just numbers.** Every step in an approach's evolution is explained through four questions: which **assumption** changed, by what **mechanism**, at what **price**, and in which **regime** the new approach wins. Reported numbers serve only as evidence.
- **Transparent, reusable search.** All queries, hit counts and before/after-filtering totals are recorded in a search log you can reuse.
- **Multi-signal core-paper selection.** Combines multi-query hits, age-adjusted citations, citations by surveys and use as a baseline, so recent work is not penalised for having few citations yet.
- **Self-check and re-search.** Checks that every framing is covered, that no theme rests on a single paper or group, and that the last 12–18 months are represented; searches again if not.
- **Escapes the home field.** Abstracts each approach into a domain-free problem, finds improved versions in other disciplines, and assesses whether they transfer back.
- **Honest labelling.** Distinguishes *claimed*, *demonstrated* and *inferred* conclusions, marks each reference as read in full, read as abstract, or only seen cited, and never invents sources.

## Modes

| Mode | Best for | How to trigger |
|---|---|---|
| **Quick** | A first overview of an unfamiliar field | Ask for a "quick overview" or "brief scan" |
| **Standard** | A general literature review (default) | Ask normally |
| **Deep** | Theses, proposals, related-work sections | Ask for a "thorough" or "comprehensive" review |
| **Trace** | Following how a specific paper or approach evolved | Name the paper or approach and ask how it developed |

## Installation

### Claude.ai / Claude desktop app
1. Download `landscape-lineage-review.zip` from the [Releases page](https://github.com/Louis-Chenyang-Lu/landscape-lineage-review/releases), or build it yourself:
   ```bash
   git clone https://github.com/Louis-Chenyang-Lu/landscape-lineage-review.git
   cd landscape-lineage-review/skills
   zip -r landscape-lineage-review.zip landscape-lineage-review
   ```
2. Upload the zip as a skill in Claude. The menu location can change between versions; see the official guide: [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).
3. Make sure web search is enabled.

### Claude Code
```bash
git clone https://github.com/Louis-Chenyang-Lu/landscape-lineage-review.git
mkdir -p ~/.claude/skills
cp -r landscape-lineage-review/skills/landscape-lineage-review ~/.claude/skills/
```

### OpenAI Codex (CLI / IDE extension / ChatGPT desktop app)
```bash
git clone https://github.com/Louis-Chenyang-Lu/landscape-lineage-review.git
mkdir -p ~/.agents/skills
cp -r landscape-lineage-review/skills/landscape-lineage-review ~/.agents/skills/
```
Restart Codex after installing. Trigger the skill in natural language or invoke it explicitly with `$landscape-lineage-review`. To use it in a single project only, copy it into that project's `.agents/skills/` instead. Allow Codex network access, since both web search and the helper script need it; if the sandbox blocks the network, the script reports the failure and the skill falls back to web search. See the [Codex skills documentation](https://developers.openai.com/codex/skills).

### Optional
Set a Semantic Scholar API key for higher rate limits on citation lookups:
```bash
export S2_API_KEY=<your_key>
```

## Quick start

```
Do a literature review on <your research topic>.
My data / setting: <brief description>. I care most about <a question or limitation>.
```

The skill replies in the language you write in. More: [Usage guide](docs/usage-guide.md) · [Prompt templates](examples/prompts.md) · [Design notes](docs/design.md)

## Repository structure

```
skills/landscape-lineage-review/
├── SKILL.md                    # Workflow and rules
├── agents/openai.yaml          # Display metadata for Codex / ChatGPT (ignored by Claude)
├── references/templates.md     # Search log, core-paper table, theme card,
│                               # principle card, transition statement, transfer card
└── scripts/scholar_tool.py     # Multi-query retrieval and citation chaining
                                # (Semantic Scholar / OpenAlex, Python standard library only)
docs/
├── usage-guide.md              # How to use it and read the results
└── design.md                   # Design rationale and trade-offs
examples/prompts.md             # Copy-paste prompt templates
```

## Limitations

- **Slower than dedicated review tools.** A Standard review runs dozens of searches; use Quick mode when you only need an overview.
- **Public sources only.** Web search plus Semantic Scholar / OpenAlex (and any scholarly search tools connected to your agent); no proprietary paper index. Paywalled full texts are usually accessible only as abstracts.
- **A map, not a finished review.** Conclusions marked *inferred* and references marked "only seen cited" need your own verification and reading.
- **Not a systematic review.** For reviews that must follow PRISMA or similar protocols, use a dedicated workflow.

## 中文摘要

**它做什么。** 第一阶段（Landscape，广度）扩展检索词、广泛检索并去重，综合多个信号挑选核心文献，归纳主题、时间线和学术争论；覆盖不足时自动补检，最后选出值得深挖的锚点。第二阶段（Lineage，深度）从锚点出发，通过引用图、由局限反推修复方案、按问题框架检索这三个通道向前追踪，每一步都讲清"改了什么假设、靠什么机制、付出什么代价、什么条件下更好"，并把方法抽象成与领域无关的问题，到其他学科寻找更好的版本、判断能否迁移回来。最后输出覆盖度审计，以及"地图上的空白"和"机制上的空白"两类研究空白。

**四种模式。** Quick（快速全景）、Standard（默认）、Deep（深挖，适合学位论文和开题）、Trace（追踪某篇论文或某个方法的演进）。

**安装。** Claude.ai / 桌面端：从 [Releases](https://github.com/Louis-Chenyang-Lu/landscape-lineage-review/releases) 下载 zip 后上传为技能。Claude Code：复制到 `~/.claude/skills/`。Codex：复制到 `~/.agents/skills/` 后重启，并允许联网。

**语言。** 用中文提问，结果就用中文输出；论文标题和术语保留英文，方便检索原文。

## Acknowledgements

The Phase 1 workflow draws on the literature-review approach publicly described by the AI research tool [Liner](https://liner.com): query expansion, core-paper tracing, theme and gap mapping, and iterative self-evaluation. This project is not affiliated with Liner.

## License

MIT. See [LICENSE](LICENSE).
