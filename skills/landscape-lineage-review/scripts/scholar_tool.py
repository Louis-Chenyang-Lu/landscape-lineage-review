#!/usr/bin/env python3
"""
Scholarly retrieval helper for the landscape-lineage-review skill.

Backends:
  s2        Semantic Scholar Graph API (default). Gives citation contexts (the sentence in
            which a citing paper cites the node). Set S2_API_KEY for higher rate limits.
  openalex  OpenAlex API. Fallback when S2 is blocked or rate-limited; no citation contexts.

Modes:
  search    "<query>"                       single query, top results
  landscape "<q1>" "<q2>" ... | --file F    Phase 1: run many queries, deduplicate, and rank
                                            papers by how many queries found them and by
                                            citations relative to age
  forward   <id>                            Phase 2: papers citing <id>, ranked by signals of
                                            "extends / fixes / compares against"
  backward  <id>                            papers cited by <id>

<id>: S2 paperId, DOI:10.xxx, ARXIV:xxxx (s2)  |  OpenAlex W-id or DOI:10.xxx (openalex)

Examples (placeholders):
  python scholar_tool.py landscape "<core term>" "<synonym>" "<core term> survey" --since <year>
  python scholar_tool.py landscape --file queries.txt --backend openalex --json out.json
  python scholar_tool.py forward DOI:<doi> --top 25 --since <year>

If a backend fails the script says so and exits with code 2: treat that as
"channel failed", never as "nothing exists".
"""
import json, os, re, sys, time, argparse, urllib.parse, urllib.request, urllib.error

SIGNAL = re.compile(
    r"\b(limitation|limited|however|unlike|fail\w*|suffer\w*|drawback|shortcoming|"
    r"cannot|unable|restrict\w*|assum\w*|bias\w*|improv\w*|extend\w*|overcome|"
    r"address\w*|alleviat\w*|instead|in contrast|remed\w*|mitigat\w*|beyond|"
    r"generaliz\w*|baseline\w*|compar\w*|outperform\w*|competing|state[- ]of[- ]the[- ]art)\b",
    re.I)


def http_json(url, headers=None, retries=5):
    headers = {"User-Agent": "landscape-lineage-review/1.0", **(headers or {})}
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < retries - 1:
                time.sleep(2 ** i * 2); continue
            raise


# ---------------- Semantic Scholar ----------------
S2 = "https://api.semanticscholar.org/graph/v1"
S2F = "title,year,venue,citationCount,externalIds,url"


def s2_get(path, params):
    h = {"x-api-key": os.environ["S2_API_KEY"]} if os.environ.get("S2_API_KEY") else {}
    return http_json(f"{S2}{path}?{urllib.parse.urlencode(params)}", h)


def s2_search(q, n=10):
    return [norm_s2(p) for p in s2_get("/paper/search", {"query": q, "limit": min(100, n), "fields": S2F}).get("data", [])]


def s2_links(pid, kind, limit):
    key = "citingPaper" if kind == "citations" else "citedPaper"
    fields = "contexts,intents,isInfluential," + ",".join(f"{key}.{f}" for f in S2F.split(",")) + f",{key}.paperId"
    out, off = [], 0
    while off < limit:
        res = s2_get(f"/paper/{pid}/{kind}", {"fields": fields, "limit": min(100, limit - off), "offset": off})
        data = res.get("data", [])
        for d in data:
            p = norm_s2(d.get(key) or {})
            p.update(contexts=d.get("contexts") or [], intents=d.get("intents") or [], influential=bool(d.get("isInfluential")))
            out.append(p)
        if "next" not in res or not data: break
        off = res["next"]; time.sleep(1)
    return out


def norm_s2(p):
    ids = p.get("externalIds") or {}
    return {"id": p.get("paperId"), "title": p.get("title"), "year": p.get("year"), "venue": p.get("venue"),
            "cites": p.get("citationCount"), "doi": ids.get("DOI"), "arxiv": ids.get("ArXiv"),
            "url": p.get("url"), "text": ""}


# ---------------- OpenAlex ----------------
OA = "https://api.openalex.org"


def oa_get(path, params):
    return http_json(f"{OA}{path}?{urllib.parse.urlencode(params)}")


def oa_abstract(inv):
    if not inv: return ""
    pos = {i: w for w, idxs in inv.items() for i in idxs}
    return " ".join(pos[i] for i in sorted(pos))


def norm_oa(w):
    return {"id": (w.get("id") or "").rsplit("/", 1)[-1], "title": w.get("display_name"), "year": w.get("publication_year"),
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "cites": w.get("cited_by_count"), "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
            "arxiv": None, "url": w.get("doi") or w.get("id"), "text": oa_abstract(w.get("abstract_inverted_index")),
            "contexts": [], "intents": [], "influential": False}


def oa_resolve(pid):
    if pid.upper().startswith("DOI:"):
        return oa_get(f"/works/doi:{pid[4:]}", {})["id"].rsplit("/", 1)[-1]
    return pid


def oa_search(q, n=10):
    return [norm_oa(w) for w in oa_get("/works", {"search": q, "per-page": min(200, n)}).get("results", [])]


def oa_links(pid, kind, limit):
    wid = oa_resolve(pid)
    if kind == "references":
        refs = oa_get(f"/works/{wid}", {}).get("referenced_works", [])[:limit]
        out = []
        for i in range(0, len(refs), 50):
            ids = "|".join(r.rsplit("/", 1)[-1] for r in refs[i:i + 50])
            out += [norm_oa(w) for w in oa_get("/works", {"filter": f"openalex:{ids}", "per-page": 50}).get("results", [])]
        return out
    out, cursor = [], "*"
    while cursor and len(out) < limit:
        res = oa_get("/works", {"filter": f"cites:{wid}", "per-page": 100, "cursor": cursor, "sort": "cited_by_count:desc"})
        out += [norm_oa(w) for w in res.get("results", [])]
        cursor = (res.get("meta") or {}).get("next_cursor"); time.sleep(0.5)
    return out[:limit]


# ---------------- ranking / output ----------------
def score(p, since):
    if since and (p.get("year") or 0) < since: return None
    txt = " ".join(p.get("contexts") or []) + " " + (p.get("title") or "") + " " + (p.get("text") or "")
    s = 3 * len(SIGNAL.findall(txt)) + (5 if p.get("influential") else 0)
    s += 2 * sum(1 for i in p.get("intents") or [] if i in ("methodology", "result"))
    s += min(5, (p.get("cites") or 0) ** 0.5 / 4)
    s += 2 if (p.get("year") or 0) >= time.gmtime().tm_year - 1 else 0   # recency bonus
    return s


def fmt(p):
    tag = f"arXiv:{p['arxiv']}" if p.get("arxiv") else (f"DOI:{p['doi']}" if p.get("doi") else "")
    return f"{p.get('title')} ({p.get('year')}, {p.get('venue') or '-'}) cites={p.get('cites')} {tag}\n    id={p.get('id')} {p.get('url') or ''}"


def landscape(queries, backend, per_query, since):
    """Run several queries, merge duplicates, count multi-query hits, rank."""
    fn = s2_search if backend == "s2" else oa_search
    merged, failures = {}, []
    for q in queries:
        try:
            res = fn(q, per_query)
        except Exception as e:
            failures.append((q, str(e)))
            continue
        for p in res:
            key = (p.get("doi") or "").lower() or (p.get("arxiv") or "") or \
                  re.sub(r"\W+", " ", (p.get("title") or "").lower()).strip()
            if not key:
                continue
            m = merged.setdefault(key, {**p, "queries": []})
            if q not in m["queries"]:
                m["queries"].append(q)
        time.sleep(1 if backend == "s2" else 0.3)
    year_now = time.gmtime().tm_year
    rows = []
    for p in merged.values():
        y = p.get("year") or 0
        if since and y and y < since:
            continue
        age = max(1, year_now - y + 1) if y else 10
        cpy = (p.get("cites") or 0) / age
        p["cites_per_year"] = round(cpy, 1)
        p["score"] = round(3 * len(p["queries"]) + min(6, cpy ** 0.5), 2)
        rows.append(p)
    rows.sort(key=lambda r: -r["score"])
    return rows, failures


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["search", "landscape", "forward", "backward"])
    ap.add_argument("args", nargs="*", help="query / queries / paper id")
    ap.add_argument("--file", help="landscape: text file with one query per line")
    ap.add_argument("--backend", choices=["s2", "openalex"], default="s2")
    ap.add_argument("--per-query", type=int, default=20, help="landscape/search: results per query")
    ap.add_argument("--limit", type=int, default=300, help="forward/backward: max links fetched")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--since", type=int, default=0)
    ap.add_argument("--json", help="also write full results to this JSON file")
    a = ap.parse_args()

    if a.mode == "landscape":
        qs = list(a.args)
        if a.file:
            qs += [l.strip() for l in open(a.file, encoding="utf-8") if l.strip() and not l.startswith("#")]
        if not qs:
            ap.error("landscape needs queries (positional or --file)")
        rows, failures = landscape(qs, a.backend, a.per_query, a.since)
        for q, err in failures:
            print(f"CHANNEL FAILED ({a.backend}) for query {q!r}: {err}", file=sys.stderr)
        if failures and len(failures) == len(qs):
            print("-> every query failed: try the other --backend, then web search. "
                  "Do NOT conclude that nothing exists.", file=sys.stderr)
            sys.exit(2)
        print(f"{len(qs)} queries via {a.backend}: {len(rows)} unique papers after deduplication "
              f"({len(failures)} queries failed)")
        for r in rows[:a.top]:
            print(f"\n[{r['score']}] hits={len(r['queries'])} cites/yr={r['cites_per_year']} {fmt(r)}")
            print("    found by:", " | ".join(r["queries"][:5]))
        if a.json:
            json.dump(rows, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"\nfull results written to {a.json}")
        return

    if not a.args:
        ap.error(f"{a.mode} needs an argument")
    arg = a.args[0] if a.mode != "search" else " ".join(a.args)
    try:
        if a.mode == "search":
            for p in (s2_search if a.backend == "s2" else oa_search)(arg, a.per_query):
                print("-", fmt(p))
            return
        kind = "citations" if a.mode == "forward" else "references"
        items = (s2_links if a.backend == "s2" else oa_links)(arg, kind, a.limit)
    except Exception as e:
        print(f"CHANNEL FAILED ({a.backend}): {e}\n-> try the other --backend, then web search. "
              "Do NOT conclude that nothing exists.", file=sys.stderr)
        sys.exit(2)
    print(f"{len(items)} {kind} fetched via {a.backend}")
    scored = [(score(p, a.since), p) for p in items]
    ranked = sorted([x for x in scored if x[0] is not None], key=lambda x: -x[0])[:a.top]
    for s, p in ranked:
        print(f"\n[{s:.1f}]{' [influential]' if p.get('influential') else ''} {fmt(p)}")
        for c in (p.get("contexts") or [])[:3]:
            print("    >", re.sub(r"\s+", " ", c)[:400])
        if not p.get("contexts") and p.get("text"):
            print("    abstract:", p["text"][:300])
    if a.json:
        json.dump([p for _, p in ranked], open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
