"""nikunj-mode toolkit. Stdlib only. Exit code 1 when anything FAILs.

  python verify.py merge   OUT.md PART1.md PART2.md ...   # merge research parts, renumber E# globally, drop duplicates
  python verify.py fields  RESEARCH.md [--ids E1,E5] [--keys Claim,Limits] [--status pending]
                                                          # compact view; use instead of reading RESEARCH.md
  python verify.py sources RESEARCH.md [--ids E61,E62]    # exists? title matches? URL alive? quote on page?
  python verify.py claims  IDEA.md WORKDIR                # every number tagged; every tag resolves; E tags verified

Entry header: '### E12 | <exact title> | <year>'. Fields one per line: 'Name: value'.
"""
import difflib, html, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

UA = {"User-Agent": "nikunj-mode-verify/2.0 (research citation checker; mailto:none)"}
HEAD = re.compile(r"^###\s+(E\d+)\s*\|\s*(.+?)\s*\|\s*(\d{4})\s*$", re.M)
OK_VERDICTS = ("yes", "corrected")


# ---------- parsing ----------
def entries(text):
    heads = list(HEAD.finditer(text))
    out = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[h.end():end]
        # stop at the next non-entry heading (e.g. '## Failure map')
        m = re.search(r"^#{1,2}\s", body, re.M)
        tail = body[m.start():] if m else ""
        body = body[:m.start()] if m else body
        fields = {}
        for line in body.splitlines():
            fm = re.match(r"^([A-Za-z]+):\s*(.*)$", line)
            if fm:
                fields[fm.group(1).lower()] = fm.group(2).strip()
        out.append(dict(id=h.group(1), title=h.group(2), year=h.group(3), f=fields,
                        raw=text[h.start():h.end()] + body, tail=tail))
    return out


def verdict(e):
    return (e["f"].get("verified", "pending").split(":")[0].split()[0] if e["f"].get("verified") else "pending").lower()


def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", re.sub(r"[^\w%.\s]", " ", s.lower())).strip()


def sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


# ---------- network ----------
def get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read()


def fetchable(url):
    """Rewrite bot-hostile hosts (PMC, PubMed) to Europe PMC REST, which serves plain text."""
    m = re.search(r"(PMC\d+)", url)
    if m and ("ncbi.nlm.nih.gov" in url or "europepmc" in url):
        return f"https://www.ebi.ac.uk/europepmc/webservices/rest/{m.group(1)}/fullTextXML"
    m = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", url)
    if m:
        return ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?resultType=core&format=json&query="
                + urllib.parse.quote(f"EXT_ID:{m.group(1)} AND SRC:MED"))
    return url


def quote_on_page(quote, page):
    q, p = norm(quote), norm(page)
    if not q:
        return False
    if q in p:
        return True
    m = difflib.SequenceMatcher(None, p, q, autojunk=False).find_longest_match(0, len(p), 0, len(q))
    return m.size >= 0.8 * len(q)


def arxiv_title(aid):
    aid = re.sub(r"v\d+$", "", aid.strip())
    _, _, body = get(f"http://export.arxiv.org/api/query?id_list={aid}")
    xml = body.decode("utf-8", "ignore")
    titles = re.findall(r"<title>(.*?)</title>", xml, re.S)
    pub = re.search(r"<published>(\d{4})", xml)
    if len(titles) < 2:
        return None, None
    return re.sub(r"\s+", " ", titles[1]).strip(), pub.group(1) if pub else None


def doi_title(doi):
    _, _, body = get("https://api.crossref.org/works/" + urllib.parse.quote(doi.strip()))
    msg = json.loads(body)["message"]
    year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return (msg.get("title") or [""])[0], str(year) if year else None


def search_title(title):
    """Europe PMC first (no rate limit trouble), Crossref second. Semantic Scholar is not used: it 429s."""
    best, byear = None, None
    try:
        q = urllib.parse.quote(f'TITLE:"{title}"')
        _, _, body = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json&pageSize=5")
        for h in json.loads(body).get("resultList", {}).get("result", []):
            if best is None or sim(h.get("title", ""), title) > sim(best, title):
                best, byear = h.get("title", ""), h.get("pubYear")
    except Exception:
        pass
    if best is None or sim(best, title) < 0.85:
        try:
            q = urllib.parse.quote(title)
            _, _, body = get(f"https://api.crossref.org/works?query.bibliographic={q}&rows=5&select=title,issued")
            for h in json.loads(body)["message"]["items"]:
                t = (h.get("title") or [""])[0]
                if best is None or sim(t, title) > sim(best, title):
                    best = t
                    byear = str((h.get("issued", {}).get("date-parts") or [[None]])[0][0])
        except Exception:
            pass
    return best, byear


# ---------- commands ----------
def cmd_sources(path, ids=None):
    es = entries(Path(path).read_text(encoding="utf-8"))
    if ids:
        es = [e for e in es if e["id"] in ids]
    if not es:
        print("FAIL no entries found. Header format: '### E1 | <exact title> | <year>'")
        return 1
    rows, fails = [], 0
    for e in es:
        f, title, year = e["f"], e["title"], e["year"]
        kind = (f.get("kind") or "paper").lower()
        quote = f.get("quote", "").strip().strip('"“”')
        status, notes = "PASS", []

        found, fyear, src = None, None, None
        try:
            if f.get("arxiv"):
                src = "arXiv"; found, fyear = arxiv_title(f["arxiv"])
            elif f.get("doi"):
                src = "Crossref"; found, fyear = doi_title(f["doi"])
            elif kind == "paper":
                src = "EuropePMC/Crossref"; found, fyear = search_title(title); time.sleep(0.3)
        except Exception as ex:
            src = "error"; notes.append(f"lookup error {type(ex).__name__}")
        if src == "error":
            status = "CHECK"
        elif src:
            if not found:
                status = "FAIL"; notes.append(f"not found on {src}")
            elif sim(found, title) < 0.85:
                status = "FAIL"; notes.append(f"title mismatch on {src}: '{found[:80]}'")
            elif fyear and fyear != "None" and abs(int(fyear) - int(year)) > 1:
                status = "WARN"; notes.append(f"year {year} vs {src} {fyear}")

        url = f.get("url", "")
        if not url:
            status = "FAIL"; notes.append("no URL")
        else:
            try:
                _, ctype, body = get(fetchable(url))
                text = body.decode("utf-8", "ignore")
                if "pdf" in ctype.lower() or url.lower().endswith(".pdf"):
                    notes.append("PDF: quote needs manual check")
                    status = "CHECK" if status == "PASS" else status
                elif not quote:
                    status = "FAIL"; notes.append("no Quote")
                elif re.search(r"recaptcha|are you a robot|captcha", text[:5000], re.I):
                    notes.append("bot wall: give a Europe PMC / arXiv / DOI URL instead")
                    status = "CHECK" if status == "PASS" else status
                elif not quote_on_page(quote, text):
                    notes.append("quote not on page (JS page or paraphrase?)")
                    status = "CHECK" if status == "PASS" else status
            except Exception as ex:
                status = "FAIL"; notes.append(f"URL dead: {type(ex).__name__} {getattr(ex, 'code', '')}".strip())
        fails += status == "FAIL"
        if status != "PASS":
            rows.append((e["id"], status, title[:60], "; ".join(notes)))

    statuses = [r[1] for r in rows]
    n = {s: statuses.count(s) for s in ("WARN", "CHECK", "FAIL")}
    if rows:  # only non-PASS rows printed, to keep output small
        print("| E# | Status | Title | Notes |\n|---|---|---|---|")
        for r in rows:
            print("| " + " | ".join(r) + " |")
    print(f"{len(es)} entries: PASS {len(es) - len(rows)}, " + ", ".join(f"{k} {v}" for k, v in n.items()))
    return 1 if fails else 0


def cmd_fields(path, ids=None, keys=None, status=None):
    es = entries(Path(path).read_text(encoding="utf-8"))
    for e in es:
        if ids and e["id"] not in ids:
            continue
        if status and verdict(e) != status:
            continue
        if keys == ["all"]:
            print(e["raw"].strip() + "\n")
            continue
        parts = [f"{e['id']} | {e['title'][:90]} | {e['year']} | {verdict(e)}"]
        for k in keys or []:
            parts.append(f"{k}: {e['f'].get(k.lower(), '')}")
        print(" || ".join(parts))
    return 0


def _key(e):
    f = e["f"]
    if f.get("arxiv"):
        return "arxiv:" + re.sub(r"v\d+$", "", f["arxiv"].strip())
    if f.get("doi"):
        return "doi:" + f["doi"].lower().strip()
    return "title:" + norm(e["title"])


def cmd_merge(out, parts):
    """Each part numbers its own entries E1..En. Merge renumbers globally, drops duplicates
    (same arXiv id, DOI, or normalized title) and rewrites [E#] refs inside each kept entry."""
    kept, seen, log = [], {}, []
    for p in parts:
        es = entries(Path(p).read_text(encoding="utf-8"))
        local = {}
        for e in es:  # pass 1: assign global ids for this part
            k = _key(e)
            if k in seen:
                local[e["id"]] = seen[k]
                log.append(f"{Path(p).name}:{e['id']} duplicate of {seen[k]}")
            else:
                seen[k] = local[e["id"]] = f"E{len(seen) + 1}"
        done = set()
        for e in es:  # pass 2: rewrite ids with this part's mapping
            nid = local[e["id"]]
            if nid in done or any(nid == x[0] for x in kept):
                continue
            done.add(nid)
            raw = re.sub(r"\bE\d+\b", lambda m: local.get(m.group(0), m.group(0)), e["raw"])
            kept.append((nid, raw.strip()))
    Path(out).write_text("# Research\n\n" + "\n\n".join(r for _, r in kept) + "\n", encoding="utf-8")
    print(f"merged {len(kept)} entries from {len(parts)} parts into {out}; {len(log)} duplicates dropped")
    for line in log:
        print("  " + line)
    return 0


NUM = re.compile(r"\d+(?:\.\d+)?\s*%|\b0\.\d+\b|\b\d+(?:\.\d+)?\s*[x×]\b|\b\d+(?:\.\d+)?\s*(?:k|M|B|ms|s|GB|hours?)\b")
TAG = re.compile(r"\[((?:E|D|X|A|P)\d+)\]")
SOURCES = (("RESEARCH.md", "E"), ("DATA.md", "D"), ("EXPERIMENTS.md", "X"), ("ASSUMPTIONS.md", "A"), ("REQUIREMENTS.md", "P"))


def cmd_claims(idea, workdir):
    wd = Path(workdir)
    known, unverified = set(), {}
    for name, prefix in SOURCES:
        p = wd / name
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        if prefix == "E":
            for e in entries(t):
                v = verdict(e)
                if v in OK_VERDICTS:
                    known.add(e["id"])
                else:
                    unverified[e["id"]] = v
        else:
            known.update(m.group(1) for m in re.finditer(rf"^#+\s*({prefix}\d+)\b", t, re.M))
    fails, in_code = 0, False
    for ln, line in enumerate(Path(idea).read_text(encoding="utf-8").splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.lstrip().startswith("#"):
            continue
        tags = TAG.findall(line)
        for t in tags:
            if t in unverified:
                print(f"FAIL L{ln}: [{t}] is '{unverified[t]}', not verified: {line.strip()[:90]}")
                fails += 1
            elif t not in known:
                print(f"FAIL L{ln}: tag [{t}] not found: {line.strip()[:90]}")
                fails += 1
        if NUM.search(line) and not tags:
            print(f"FAIL L{ln}: number without source tag: {line.strip()[:90]}")
            fails += 1
    print(f"{fails} claim problems. Tags: [E#] verified source, [D#] data, [X#] experiment, [A#] assumption, [P#] problem statement.")
    return 1 if fails else 0


def opt(name):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1]
    return None


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    cmd = sys.argv[1]
    ids = set(opt("--ids").split(",")) if opt("--ids") else None
    if cmd == "sources":
        sys.exit(cmd_sources(sys.argv[2], ids))
    if cmd == "fields":
        keys = opt("--keys").split(",") if opt("--keys") else None
        sys.exit(cmd_fields(sys.argv[2], ids, keys, opt("--status")))
    if cmd == "merge":
        sys.exit(cmd_merge(sys.argv[2], [a for a in sys.argv[3:] if not a.startswith("--")]))
    if cmd == "claims":
        sys.exit(cmd_claims(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else str(Path(sys.argv[2]).parent)))
    print(__doc__); sys.exit(2)
