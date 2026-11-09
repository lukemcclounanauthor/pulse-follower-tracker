
import json
import os
import urllib.request
import urllib.error
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# PULSE FOLLOWER TRACKER
# Royal Road Fiction ID: 194924
# ==========================================

KEY = os.environ["APISH_KEY"]

URL = "https://api.api.sh/royalroad/v1/fiction?id=194924"

# ==========================================
# FETCH FOLLOWER DATA
# ==========================================

req = urllib.request.Request(
    URL,
    headers={
        "x-api-key": KEY,
        "User-Agent": "PulseFollowerTracker/2.0",
        "Accept": "application/json"
    }
)

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.load(response)

except urllib.error.HTTPError as e:
    raise RuntimeError(
        f"API request failed with HTTP {e.code}. "
        "Check your API key, endpoint and subscription."
    ) from None

except urllib.error.URLError as e:
    raise RuntimeError(
        f"Could not connect to API: {e.reason}"
    ) from None


# ==========================================
# FIND FOLLOWER COUNT
# ==========================================

def find_followers(value):
    if isinstance(value, dict):

        # Check the current object
        for key in (
            "followers",
            "follower_count",
            "followersCount"
        ):
            v = value.get(key)

            if isinstance(v, int) and not isinstance(v, bool):
                return v

            if isinstance(v, str) and v.strip().isdigit():
                return int(v.strip())

        # Search known API response structures
        for key in (
            "stats",
            "fiction",
            "data",
            "result",
            "raw"
        ):
            if key in value:
                found = find_followers(value[key])

                if found is not None:
                    return found

    return None


followers = find_followers(payload)

if followers is None or followers < 0:

    print(
        "API response keys:",
        list(payload.keys())
        if isinstance(payload, dict)
        else type(payload).__name__
    )

    raise ValueError(
        "Could not locate a valid follower count "
        "in the API response. Check the response "
        "structure or API authentication."
    )


# ==========================================
# CALCULATE BONUS CHAPTER MILESTONES
# ==========================================

unlocked = followers // 100
progress = followers % 100
next_goal = (unlocked + 1) * 100

print(f"Pulse followers: {followers}")
print(f"Bonus chapters unlocked: {unlocked}")
print(f"Progress: {progress}/100")
print(f"Next milestone: {next_goal}")


# ==========================================
# IMAGE SETTINGS
# ==========================================

W = 1000
H = 220

BACKGROUND = "#241e34"
BORDER = "#b787df"
TEXT = "#e9d2ff"
MUTED = "#cfc2dd"
WHITE = "#ffffff"
BAR_BACKGROUND = "#3b304a"

im = Image.new("RGB", (W, H), BACKGROUND)
d = ImageDraw.Draw(im)


# ==========================================
# FONT HELPERS
# ==========================================

def font(size, bold=False):

    paths = [
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
        (
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
        )
    ]

    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def centre(text, y, f, fill):

    box = d.textbbox((0, 0), text, font=f)

    width = box[2] - box[0]

    d.text(
        ((W - width) / 2, y),
        text,
        font=f,
        fill=fill
    )


def right(text, x, y, f, fill):

    box = d.textbbox((0, 0), text, font=f)

    width = box[2] - box[0]

    d.text(
        (x - width, y),
        text,
        font=f,
        fill=fill
    )


# ==========================================
# DRAW TRACKER
# ==========================================

# Outer border
d.rounded_rectangle(
    (2, 2, W - 3, H - 3),
    radius=18,
    outline=BORDER,
    width=3
)

# Bonus chapter headline
centre(
    "+1 BONUS CHAPTER EVERY 100 FOLLOWERS",
    18,
    font(28, True),
    TEXT
)

# Divider
d.line(
    (30, 65, W - 30, 65),
    fill="#624878",
    width=2
)

# Total followers
d.text(
    (34, 78),
    "TOTAL FOLLOWERS",
    font=font(17, True),
    fill=MUTED
)

d.text(
    (34, 104),
    f"{followers:,}",
    font=font(38, True),
    fill=WHITE
)

# Next milestone
right(
    "NEXT UNLOCK",
    W - 34,
    78,
    font(17, True),
    MUTED
)

right(
    f"{next_goal:,} followers",
    W - 34,
    104,
    font(38, True),
    TEXT
)

# Progress bar background
d.rounded_rectangle(
    (34, 160, W - 34, 174),
    radius=7,
    fill=BAR_BACKGROUND
)

# Progress bar fill
if progress > 0:

    bar_width = round((W - 68) * progress / 100)

    d.rounded_rectangle(
        (34, 160, 34 + bar_width, 174),
        radius=7,
        fill=BORDER
    )

# Progress label
centre(
    f"{progress} / 100 towards the next bonus chapter",
    185,
    font(18),
    MUTED
)


# ==========================================
# SAVE OUTPUT FILES
# ==========================================

output = Path("docs")
output.mkdir(exist_ok=True)

image_path = output / "progress.png"
status_path = output / "status.json"

im.save(image_path, optimize=True)

status = {
    "fiction_id": 194924,
    "followers": followers,
    "bonus_chapters_unlocked": unlocked,
    "progress": progress,
    "next_goal": next_goal
}

status_path.write_text(
    json.dumps(status, indent=2) + "\n",
    encoding="utf-8"
)

print("Successfully generated:")
print(f" - {image_path}")
print(f" - {status_path}")
print("Pulse follower tracker updated successfully!")
