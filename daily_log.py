
import random
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
now = datetime.now(IST)

# Randomly choose between 1 and 10
commit_count = random.randint(1, 10)

# Unique folder for every workflow execution
run_id = now.strftime("%Y-%m-%d-%H-%M-%S")
folder = Path("logs") / f"practice-{run_id}"

folder.mkdir(parents=True, exist_ok=True)

print(f"Random commit target: {commit_count}")
print(f"Run ID: {run_id}")

for number in range(1, commit_count + 1):

    content = f"""# Git Automation Practice

Date: {now.date()}
Run: {run_id}
Practice record: {number}/{commit_count}

Learning topics:
- Python automation
- Git commits
- GitHub Actions
- CI/CD workflows

This is a synthetic learning record.
"""

    file = folder / f"commit-{number:02d}.md"

    file.write_text(content, encoding="utf-8")

    print(f"Created: {file}")

print(f"Successfully generated {commit_count} records.")
