#!/usr/bin/env python3
"""Renders Soumik's profile artwork from live GitHub data.

Pulls contribution calendar + language breakdown via GraphQL, then draws
a blueprint-style engineering schematic of the account. Falls back to
sample data when no token is present so it can be developed offline.
"""
import os, json, math, urllib.request, datetime, random

USER  = os.environ.get("GH_USER", "Sd474")
TOKEN = os.environ.get("GH_TOKEN", "")
OUT   = os.environ.get("OUT_DIR", "assets/gen")

QUERY = """
query($login:String!){
  user(login:$login){
    createdAt
    repositories(first:100, ownerAffiliations:OWNER, isFork:false){
      totalCount
      nodes{ name stargazerCount primaryLanguage{ name color } languages(first:8, orderBy:{field:SIZE,direction:DESC}){ edges{ size node{ name color } } } }
    }
    contributionsCollection{
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount weekday } }
      }
    }
  }
}"""

def fetch():
    if not TOKEN:
        return None
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": "profile-render"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]["user"]

def sample():
    random.seed(7)
    weeks = []
    d = datetime.date.today() - datetime.timedelta(days=364)
    for w in range(53):
        days = []
        for wd in range(7):
            if d > datetime.date.today(): break
            c = max(0, int(random.gauss(2.2, 3)))
            days.append({"date": d.isoformat(), "contributionCount": c, "weekday": wd})
            d += datetime.timedelta(days=1)
        if days: weeks.append({"contributionDays": days})
    return {"createdAt": "2024-02-11T00:00:00Z",
            "repositories": {"totalCount": 14, "nodes": []},
            "contributionsCollection": {
                "totalCommitContributions": 412, "totalPullRequestContributions": 23,
                "totalIssueContributions": 9,
                "contributionCalendar": {
                    "totalContributions": sum(x["contributionCount"] for w in weeks for x in w["contributionDays"]),
                    "weeks": weeks}},
            "_langs": [("Python", "#3572A5", 61.4), ("Jupyter Notebook", "#DA5B0B", 21.8),
                       ("C++", "#f34b7d", 8.9), ("HTML", "#e34c26", 4.6), ("Shell", "#89e051", 3.3)]}

def digest(u):
    cal   = u["contributionsCollection"]["contributionCalendar"]
    days  = [d for w in cal["weeks"] for d in w["contributionDays"]]
    counts= [d["contributionCount"] for d in days]
    # streaks
    cur = best = 0
    for c in counts:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    tail = 0
    for c in reversed(counts):
        if c: tail += 1
        else: break
    # languages
    if "_langs" in u:
        langs = u["_langs"]
    else:
        tot = {}
        for r in u["repositories"]["nodes"]:
            for e in r.get("languages", {}).get("edges", []):
                n = e["node"]["name"]
                tot[n] = tot.get(n, [0, e["node"]["color"] or "#7dd3fc"])
                tot[n][0] += e["size"]
        s = sum(v[0] for v in tot.values()) or 1
        langs = sorted(((k, v[1], round(v[0]/s*100, 1)) for k, v in tot.items()),
                       key=lambda t: -t[2])[:5]
    return dict(days=days, counts=counts, total=cal["totalContributions"],
                commits=u["contributionsCollection"]["totalCommitContributions"],
                prs=u["contributionsCollection"]["totalPullRequestContributions"],
                issues=u["contributionsCollection"]["totalIssueContributions"],
                repos=u["repositories"]["totalCount"], best=best, cur=tail,
                langs=langs, since=u["createdAt"][:10],
                busiest=max(counts) if counts else 0,
                active=sum(1 for c in counts if c))

if __name__ == "__main__":
    u = fetch() or sample()
    d = digest(u)
    os.makedirs(OUT, exist_ok=True)
    json.dump({k: v for k, v in d.items() if k not in ("days",)},
              open(f"{OUT}/stats.json", "w"), indent=1, default=str)
    print(json.dumps({k: d[k] for k in ("total","commits","repos","best","cur","active","busiest")}, indent=1))
    print("langs:", d["langs"][:3])

    import blueprint
    open(f"{OUT}/blueprint.svg","w").write(blueprint.build(d))
    print("wrote blueprint.svg")
