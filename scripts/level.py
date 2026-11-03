"""Generates assets/level.svg: a level card based on the user's total public commits."""
import json, os, sys, urllib.request

USER = os.environ.get("GH_USER", "Diarooll")
TOKEN = os.environ.get("GITHUB_TOKEN")

LEVELS = [  # (min commits, name)
    (0, "Rookie"), (50, "Apprentice"), (150, "Developer"),
    (300, "Builder"), (600, "Engineer"), (1000, "Architect"), (2000, "Legend"),
]


def commit_count():
    req = urllib.request.Request(
        f"https://api.github.com/search/commits?q=author:{USER}&per_page=1",
        headers={"Accept": "application/vnd.github+json",
                 **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["total_count"]


def build(commits):
    idx = max(i for i, (m, _) in enumerate(LEVELS) if commits >= m)
    lvl, name = idx + 1, LEVELS[idx][1]
    cur = LEVELS[idx][0]
    if idx + 1 < len(LEVELS):
        nxt, nxt_name = LEVELS[idx + 1]
        pct = (commits - cur) / (nxt - cur)
        foot = f"{nxt - commits} commits to {nxt_name}"
    else:
        pct, foot = 1.0, "Max level reached"
    w = 300 * pct
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="495" height="150" viewBox="0 0 495 150" role="img" aria-label="GitHub level {lvl}: {name}, {commits} commits">
  <defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#58a6ff"/><stop offset="1" stop-color="#a371f7"/></linearGradient></defs>
  <rect width="495" height="150" rx="10" fill="#0d1117" stroke="#30363d"/>
  <g font-family="Segoe UI, Ubuntu, Helvetica, Arial, sans-serif">
    <text x="25" y="38" font-size="13" fill="#8b949e" letter-spacing="1.5">GITHUB LEVEL</text>
    <text x="25" y="78" font-size="32" font-weight="700" fill="#f0f6fc">Lv. {lvl} <tspan fill="url(#g)">{name}</tspan></text>
    <text x="470" y="78" font-size="28" font-weight="700" fill="#f0f6fc" text-anchor="end">{commits}</text>
    <text x="470" y="96" font-size="12" fill="#8b949e" text-anchor="end">commits</text>
    <rect x="25" y="108" width="300" height="10" rx="5" fill="#21262d"/>
    <rect x="25" y="108" width="{w:.1f}" height="10" rx="5" fill="url(#g)"/>
    <text x="25" y="138" font-size="12" fill="#8b949e">{foot}</text>
  </g>
</svg>
'''


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else commit_count()
    os.makedirs("assets", exist_ok=True)
    with open("assets/level.svg", "w", encoding="utf-8") as f:
        f.write(build(n))
    print(f"{USER}: {n} commits")
