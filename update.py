import json, os, urllib.request, html
from pathlib import Path

API_KEY = os.environ['APISH_KEY']
url = 'https://api.api.sh/royalroad/v1/fiction?id=194924'
req = urllib.request.Request(url, headers={'x-api-key': API_KEY, 'User-Agent': 'PulseFollowerTracker/1.0'})
with urllib.request.urlopen(req, timeout=30) as response:
    payload = json.load(response)

def find_followers(value):
    if isinstance(value, dict):
        for key in ('followers', 'follower_count'):
            v = value.get(key)
            if isinstance(v, int) and not isinstance(v, bool):
                return v
        for k in ('fiction', 'raw', 'data'):
            if k in value:
                found = find_followers(value[k])
                if found is not None: return found
    return None

followers = find_followers(payload)
if followers is None or followers < 0:
    raise ValueError('Follower count missing or unexpected response; refusing to publish incorrect tracker')

unlocked = followers // 100
progress = followers % 100
next_goal = (unlocked + 1) * 100
remaining = 100 - progress
bar_width = round(560 * progress / 100)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="214" viewBox="0 0 640 214" role="img" aria-label="Pulse has {followers} followers, {unlocked} bonus chapters unlocked, {progress} of 100 followers towards the next bonus chapter">
<rect width="640" height="214" rx="14" fill="#241e34"/>
<rect x="1" y="1" width="638" height="212" rx="13" fill="none" stroke="#b787df" stroke-width="2"/>
<g font-family="Arial,Helvetica,sans-serif" text-anchor="middle">
<text x="320" y="29" font-size="17" font-weight="bold" fill="#e9d2ff">+1 BONUS CHAPTER EVERY 100 FOLLOWERS</text>
<text x="164" y="77" font-size="35" font-weight="bold" fill="#ffffff">{followers:,}</text>
<text x="164" y="97" font-size="13" fill="#cfc2dd">TOTAL FOLLOWERS</text>
<text x="477" y="77" font-size="35" font-weight="bold" fill="#e9d2ff">{unlocked}</text>
<text x="477" y="97" font-size="13" fill="#cfc2dd">BONUS CHAPTERS UNLOCKED</text>
<text x="40" y="128" font-size="14" text-anchor="start" fill="#cfc2dd">NEXT UNLOCK: {next_goal:,} FOLLOWERS</text>
<text x="600" y="128" font-size="14" text-anchor="end" fill="#e9d2ff">{progress}/100</text>
<text x="320" y="193" font-size="14" fill="#cfc2dd">{remaining} more followers until the next bonus chapter!</text>
</g>
<rect x="40" y="143" width="560" height="16" rx="8" fill="#36404c"/>
<rect x="40" y="143" width="{bar_width}" height="16" rx="8" fill="#b787df"/>
</svg>'''
Path('docs').mkdir(exist_ok=True)
Path('docs/progress.svg').write_text(svg, encoding='utf-8')
Path('docs/status.json').write_text(json.dumps({'followers': followers, 'unlocked': unlocked, 'progress': progress, 'next_goal': next_goal}, indent=2), encoding='utf-8')
print(f'Updated: {followers} followers, {unlocked} unlocked')
