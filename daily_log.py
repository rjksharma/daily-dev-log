
import random
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
today = datetime.now(IST).date()

# Randomly select 1 to 10 commits
commit_count = random.randint(1, 10)

folder = Path("logs") / f"practice-{today}"
folder.mkdir(parents=True, exist_ok=True)

# Prevent duplicate generation on the same day
existing = list(folder.glob("commit-*.md"))

if existing:
    print(f"Already generated {len(existing)} practice commits.")
    raise SystemExit(0)

print(f"Random commit target: {commit_count}")

for number in range(1, commit_count + 1):

    content = f"""# Git Automation Practice

Date: {today}
Practice commit: {number}/{commit_count}

This is a synthetic learning record created
to experiment with Python and GitHub Actions.

Topics:
- Git commit automation
- Python scripting
- GitHub Actions
- Automated repository updates

Record number: {number}
"""

    file = folder / f"commit-{number:02d}.md"
    file.write_text(content, encoding="utf-8")

    print(f"Generated: {file}")

print(f"Successfully generated {commit_count} practice records.")
