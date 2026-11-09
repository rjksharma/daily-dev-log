
import os
import json
import random
import urllib.request
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

USERNAME = os.environ["GITHUB_USERNAME"]
IST = ZoneInfo("Asia/Kolkata")

today = datetime.now(IST).date()
target_date = today - timedelta(days=1)

# Random daily commit target: 1 to 10
daily_target = random.randint(1, 10)

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Daily-Development-Logger"
}

events = []

print(f"Daily random commit target: {daily_target}")

# Fetch actual public GitHub events
for page in range(1, 11):
    url = (
        f"https://api.github.com/users/{USERNAME}/events"
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
        ).astimezone(IST).date()
        for e in batch
    )

    if oldest < target_date:
        break

descriptions = {
    "PushEvent": lambda p: (
        f"Pushed {len(p.get('commits', []))} commit(s)"
    ),
    "PullRequestEvent": lambda p: (
        f"Pull request {p.get('action', 'updated')}"
    ),
    "IssuesEvent": lambda p: (
        f"Issue {p.get('action', 'updated')}"
    ),
    "IssueCommentEvent": lambda p: (
        "Commented on an issue or pull request"
    ),
    "PullRequestReviewEvent": lambda p: (
        "Reviewed a pull request"
    ),
    "CreateEvent": lambda p: (
        "Created a repository, branch or tag"
    ),
    "ReleaseEvent": lambda p: (
        "Published a release"
    )
}

activities = []

for event in events:
    event_time = datetime.fromisoformat(
        event["created_at"].replace("Z", "+00:00")
    ).astimezone(IST)

    if event_time.date() != target_date:
        continue

    event_type = event["type"]

    if event_type not in descriptions:
        continue

    payload = event.get("payload", {})
    repo = event["repo"]["name"]

    activities.append({
        "id": event["id"],
        "time": event_time.strftime("%H:%M IST"),
        "repo": repo,
        "description": descriptions[event_type](payload),
        "type": event_type
    })

# Avoid duplicate records already saved
folder = Path("logs") / str(target_date)
folder.mkdir(parents=True, exist_ok=True)

new_activities = [
    activity for activity in activities
    if not (folder / f"event-{activity['id']}.md").exists()
]

# Select random distinct genuine activities
selected = random.sample(
    new_activities,
    min(daily_target, len(new_activities))
)

print(f"Available new activities: {len(new_activities)}")
print(f"Selected activities: {len(selected)}")

for activity in selected:
    content = f"""# Development Activity

Date: {target_date}
Time: {activity['time']}
GitHub: @{USERNAME}

## Activity

- Repository: `{activity['repo']}`
- Event: {activity['description']}
- Event type: {activity['type']}
- Event ID: {activity['id']}

This report records an actual public GitHub event.
"""

    output_file = folder / f"event-{activity['id']}.md"
    output_file.write_text(content, encoding="utf-8")

    print(f"Created: {output_file}")

if not selected:
    print("No new qualifying activity. No commits will be generated.")
