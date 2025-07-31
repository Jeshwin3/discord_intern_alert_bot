from airflow.decorators import dag, task
from airflow.models import Variable
from datetime import datetime
from pathlib import Path
import tempfile
import shutil
import logging
import requests
from git import Repo
import re

@dag(
    dag_id="github_readme_discord",
    start_date=datetime(2025, 7, 30),
    schedule="@daily",
    catchup=False,
    tags=["github", "discord", "readme"],
)
def github_readme_discord():

    @task()
    def clone_repo_and_get_readme_path() -> str:
        repo_url = "https://github.com/SimplifyJobs/Summer2026-Internships.git"
        temp_dir = Path(tempfile.mkdtemp(prefix="github_clone_"))
        logging.info(f"Cloning repo into {temp_dir}")

        try:
            Repo.clone_from(repo_url, temp_dir)
        except Exception as e:
            logging.error(f"Failed to clone repo: {e}")
            raise

        readme_path = temp_dir / "README.md"
        if not readme_path.exists():
            raise FileNotFoundError("README.md not found in the repository.")

        return str(readme_path)

    @task()
    def parse_and_format_readme(readme_path: str) -> str:
        def remove_emojis(text):
            return re.sub(r"[^\w\s,./()\-–]", "", text)

        content = Path(readme_path).read_text(encoding="utf-8")
        lines = content.splitlines()

        # Grab first 10 lines that contain internship listings
        internship_lines = [
            line for line in lines
            if line.strip().startswith("|") and "https" in line
        ][:10]

        formatted = ["**🚀 Top Internship Listings from SimplifyJobs:**"]
        for i, line in enumerate(internship_lines, 1):
            cells = [remove_emojis(c.strip()) for c in line.strip().split("|")[1:-1]]
            if len(cells) >= 3:
                company, role, location = cells[:3]
                formatted.append(f"{i}. **{company}** — *{role}* — `{location}`")
            else:
                formatted.append(f"{i}. ⚠️ Skipped malformed row")

        return "\n".join(formatted)

    @task()
    def send_to_discord(message: str):
        webhook_url = Variable.get("DISCORD_WEBHOOK_URL", default_var=None)
        if not webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL Airflow variable is not set.")

        payload = {"content": message}
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            logging.info("✅ Discord message sent successfully.")
        except Exception as e:
            logging.error(f"❌ Failed to send Discord message: {e}")
            raise

    # Task chaining
    readme_path = clone_repo_and_get_readme_path()
    internship_message = parse_and_format_readme(readme_path)
    send_to_discord(internship_message)

dag_instance = github_readme_discord()
