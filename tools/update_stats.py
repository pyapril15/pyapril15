"""Refresh assets/stats.json from your public GitHub profile pages (no token needed).
   python update_stats.py && python build.py"""
import html, json, os, re, urllib.request, datetime

USER = "pyapril15"
HERE = os.path.dirname(os.path.abspath(__file__))
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode("utf-8", "ignore")

repos, page = {}, 1
while True:
    t = get(f"https://github.com/{USER}?page={page}&tab=repositories")
    blocks = t.split('itemprop="owns"')[1:]
    if not blocks: break
    for blk in blocks:
        n = re.search(r'itemprop="name codeRepository"\s*>\s*([^<]+?)\s*</a>', blk)
        if not n: continue
        name = n.group(1).strip()
        st = re.search(r'href="/%s/%s/stargazers"[^>]*>(.*?)</a>' % (USER, re.escape(name)), blk, re.S)
        stars = int(re.sub(r"[^\d]", "", re.sub(r"<[^>]+>", "", st.group(1))) or 0) if st else 0
        lang = re.search(r'itemprop="programmingLanguage">([^<]+)<', blk)
        repos[name] = (stars, lang and html.unescape(lang.group(1)))
    if f"page={page+1}&amp;tab=repositories" not in t: break
    page += 1

prof = get(f"https://github.com/{USER}")
fol = re.search(r'<span class="text-bold color-fg-default">([\d,]+)</span>\s*followers', prof)
rep = re.search(r'Repositories\s*<span[^>]*title="([\d,]+)"', prof)
top = sorted(repos.items(), key=lambda kv: (-kv[1][0], kv[0].lower()))[:5]
stats = dict(user=USER, repos=int(rep.group(1).replace(",", "")) if rep else len(repos),
             stars=sum(v[0] for v in repos.values()), followers=int(fol.group(1).replace(",", "")) if fol else 0,
             languages=len({v[1] for v in repos.values() if v[1]}), top=[[k, v[0]] for k, v in top],
             asof=datetime.date.today().isoformat())
json.dump(stats, open(f"{HERE}/assets/stats.json", "w"), indent=1)
print(stats)
