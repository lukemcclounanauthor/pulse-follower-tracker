import json, os, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

KEY = os.environ['APISH_KEY']
URL = 'https://api.api.sh/royalroad/v1/fiction?id=194924'
req = urllib.request.Request(URL, headers={'x-api-key': KEY, 'User-Agent':'PulseFollowerTracker/2.0', 'Accept':'application/json'})
with urllib.request.urlopen(req, timeout=30) as response:
    payload = json.load(response)

def find_followers(value):
    if isinstance(value, dict):
        for key in ('followers', 'follower_count', 'followersCount'):
            v = value.get(key)
            if isinstance(v, int) and not isinstance(v, bool): return v
            if isinstance(v, str) and v.isdigit(): return int(v)
        for key in ('fiction', 'data', 'result', 'raw'):
            if key in value:
                found = find_followers(value[key])
                if found is not None: return found
    return None

followers = find_followers(payload)
if followers is None or followers < 0:
    raise ValueError('Could not locate a valid follower count in API response; no image published')

unlocked = followers // 100
progress = followers % 100
next_goal = (unlocked + 1) * 100
W, H = 1000, 220
im = Image.new('RGB', (W,H), '#241e34')
d = ImageDraw.Draw(im)
def font(size, bold=False):
    paths = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
    for path in paths:
        if Path(path).exists(): return ImageFont.truetype(path, size)
    return ImageFont.load_default()
def centre(text, y, f, fill):
    box = d.textbbox((0,0),text,font=f)
    d.text(((W-(box[2]-box[0]))/2,y),text,font=f,fill=fill)
def right(text, x, y, f, fill):
    box = d.textbbox((0,0),text,font=f)
    d.text((x-(box[2]-box[0]),y),text,font=f,fill=fill)

d.rounded_rectangle((2,2,W-3,H-3),radius=18,outline='#b787df',width=3)
centre('+1 BONUS CHAPTER EVERY 100 FOLLOWERS', 18, font(28,True),'#e9d2ff')
d.line((30,65,W-30,65),fill='#624878',width=2)
d.text((34,78),'TOTAL FOLLOWERS',font=font(17,True),fill='#cfc2dd')
d.text((34,104),f'{followers:,}',font=font(38,True),fill='#ffffff')
right('NEXT UNLOCK',W-34,78,font(17,True),'#cfc2dd')
right(f'{next_goal:,} followers',W-34,104,font(38,True),'#e9d2ff')
d.rounded_rectangle((34,160,W-34,174),radius=7,fill='#3b304a')
if progress:
    d.rounded_rectangle((34,160,34+round((W-68)*progress/100),174),radius=7,fill='#b787df')
centre(f'{progress} / 100 towards the next bonus chapter',185,font(18),'#cfc2dd')
Path('docs').mkdir(exist_ok=True)
im.save('docs/progress.png',optimize=True)
Path('docs/status.json').write_text(json.dumps({'followers':followers,'unlocked':unlocked,'progress':progress,'next_goal':next_goal},indent=2)+'\n')
print(f'Updated: {followers} followers, next milestone {next_goal}')
