
import os
import json
import urllib.request
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

username = os.environ["GITHUB_USERNAME"]
today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
target = today - timedelta(days=1)

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Daily-Dev-Logger"
}

events = []

for page in range(1, 11):
    url = (
        f"https://api.github.com/users/{username}/events"
        f"?per_page=100&page={page}"
    )

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=30) as response:
        batch = json.loads(response.read().decode())

    if not batch:
        break

    events.extend(batch)

    oldest = min(
        datetime.fromisoformat(
            e["created_at"].replace("Z", "+00:00")
        ).astimezone(ZoneInfo("Asia/Kolkata")).date()
        for e in batch
    )

    if oldest < target:
        break

activities = []

for event in events:
    time = datetime.fromisoformat(
        event["created_at"].replace("Z", "+00:00")
    ).astimezone(ZoneInfo("Asia/Kolkata"))

    if time.date() != target:
        continue

    event_type = event["type"]
    repo = event["repo"]["name"]
    payload = event.get("payload", {})

    descriptions = {
        "PushEvent": f"Pushed {len(payload.get('commits', []))} commit(s)",
        "PullRequestEvent": f"Pull request {payload.get('action', 'updated')}",
        "IssuesEvent": f"Issue {payload.get('action', 'updated')}",
        "IssueCommentEvent": "Commented on an issue or PR",
        "PullRequestReviewEvent": "Reviewed a pull request",
        "CreateEvent": "Created a repository, branch or tag",
        "ReleaseEvent": "Published a release"
    }

    description = descriptions.get(event_type)

    if description:
        activities.append(
            f"- {time.strftime('%H:%M IST')} — "
            f"{description} in `{repo}`"
        )

if not activities:
    print("No public activity found. Skipping commit.")
    raise SystemExit(0)

folder = Path("logs")
folder.mkdir(exist_ok=True)

file = folder / f"{target}.md"

content = (
    f"# Development Activity — {target}\n\n"
    f"GitHub user: @{username}\n\n"
    "## Actual GitHub activity\n\n"
    + "\n".join(activities)
    + "\n"
)

if file.exists() and file.read_text(encoding="utf-8") == content:
    print("Already recorded. Skipping.")
    raise SystemExit(0)

file.write_text(content, encoding="utf-8")
print(f"Created {file}")
  
