# Pulse follower tracker

Generates a 640×214 SVG progress panel and JSON status for Royal Road fiction 194924.

## Set-up

1. Create a GitHub repository and upload these files, retaining `.github/workflows/update.yml`.
2. Obtain an API key from https://api.sh/ (the Royal Road fiction endpoint is a third-party paid/free-tier service, not an official Royal Road API).
3. In GitHub: Settings → Secrets and variables → Actions → New repository secret, name it `APISH_KEY` and paste the key.
4. Settings → Pages → Build and deployment → Deploy from a branch; choose `main` and `/docs`.
5. Actions → Update Pulse follower tracker → Run workflow. Check that `docs/progress.svg` and `docs/status.json` are committed.
6. Your public image URL will be `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/progress.svg` (assuming Pages is enabled for this repo).
7. Insert the following in your shoutout HTML, replacing the URL:

```html
<a href="https://www.royalroad.com/fiction/194924/pulse-progression-weak-to-strong-tournament"><img src="https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/progress.svg" alt="Pulse bonus chapter follower progress" style="display:block;width:100%;max-width:640px;height:auto;margin:12px auto;"></a>
```

**Important:** Test whether Royal Road allows remote SVG images. If it blocks SVG or GitHub Pages images, use a PNG hosted at an allowed domain instead. The current code generates SVG, not PNG. Also, GitHub Actions schedules may run late, GitHub Pages deployment can lag, and images may be cached; this is periodic rather than real-time. The third-party API may change its response or pricing. Check its usage limits before enabling the schedule. Never put your API key in public code or HTML.

The counter uses `followers // 100` for unlocked bonus chapters and `followers % 100` for progress. This assumes you deliver a bonus chapter at each milestone, and does not track actual chapters published.
