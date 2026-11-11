"""Refresh assets/stats.json with live numbers.
 - In GitHub Actions (GITHUB_TOKEN set) it uses the REST API.
 - Locally, with no token, it falls back to reading your public profile pages.
   python update_stats.py && python build.py"""
import datetime, html, json, os, re, urllib.request

USER = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "pyapril15"
HERE = os.path.dirname(os.path.abspath(__file__))


def http(u, token=None, accept=None):
    h = {"User-Agent": "profile-cards"}
    if token: h["Authorization"] = f"Bearer {token}"
    if accept: h["Accept"] = accept
    return urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=30).read().decode("utf-8", "ignore")


def summarize(user, repos):
    """user: API user dict. repos: list of dicts(name, stars, lang, desc, fork, created). Pure function, easy to test."""
    own = [r for r in repos if not r["fork"]]
    top = sorted(own, key=lambda r: (-r["stars"], r["name"].lower()))[:5]
    recent = [r for r in sorted(own, key=lambda r: r["created"], reverse=True) if r["name"].lower() != USER.lower()][:5]
    return dict(user=USER, repos=user["public_repos"], stars=sum(r["stars"] for r in own), followers=user["followers"],
                languages=len({r["lang"] for r in own if r["lang"]}), top=[[r["name"], r["stars"]] for r in top],
                recent=[dict(name=r["name"], desc=r["desc"], lang=r["lang"], stars=r["stars"]) for r in recent],
                asof=datetime.date.today().isoformat())


def from_api(token):
    user = json.loads(http(f"https://api.github.com/users/{USER}", token))
    repos, page = [], 1
    while True:
        batch = json.loads(http(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}", token))
        repos += [dict(name=r["name"], stars=r["stargazers_count"], lang=r["language"], desc=r["description"], fork=r["fork"], created=r["created_at"]) for r in batch]
        if len(batch) < 100: break
        page += 1
    return summarize(user, repos)


def from_pages():
    repos, page = [], 1
    while True:
        t = http(f"https://github.com/{USER}?page={page}&tab=repositories")
        blocks = t.split('itemprop="owns"')[1:]
        if not blocks: break
        for i, blk in enumerate(blocks):
            n = re.search(r'itemprop="name codeRepository"\s*>\s*([^<]+?)\s*</a>', blk)
            if not n: continue
            name = n.group(1).strip()
            st = re.search(r'href="/%s/%s/stargazers"[^>]*>(.*?)</a>' % (USER, re.escape(name)), blk, re.S)
            lang = re.search(r'itemprop="programmingLanguage">([^<]+)<', blk)
            desc = re.search(r'itemprop="description"[^>]*>\s*(.*?)\s*</p>', blk, re.S)
            repos.append(dict(name=name, stars=int(re.sub(r"[^\d]", "", re.sub(r"<[^>]+>", "", st.group(1))) or 0) if st else 0,
                              lang=html.unescape(lang.group(1)) if lang else None,
                              desc=html.unescape(re.sub(r"<[^>]+>", "", desc.group(1)).strip()) if desc else None,
                              fork="Forked from" in blk, created=f"{9999-len(repos):05d}"))   # page order = most recently updated
        if f"page={page+1}&amp;tab=repositories" not in t: break
        page += 1
    prof = http(f"https://github.com/{USER}")
    fol = re.search(r'<span class="text-bold color-fg-default">([\d,]+)</span>\s*followers', prof)
    rep = re.search(r'Repositories\s*<span[^>]*title="([\d,]+)"', prof)
    return summarize(dict(public_repos=int(rep.group(1).replace(",", "")) if rep else len(repos), followers=int(fol.group(1).replace(",", "")) if fol else 0), repos)


if __name__ == "__main__":
    tok = os.environ.get("GITHUB_TOKEN")
    try:
        stats = from_api(tok) if tok else from_pages()
    except Exception as e:                      # API hiccup or rate limit: fall back to the public pages
        print("API failed, using profile pages:", e); stats = from_pages()
    json.dump(stats, open(f"{HERE}/assets/stats.json", "w"), indent=1)
    print(json.dumps(stats, indent=1)[:700])
