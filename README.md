
# 🚀 GitHub Internship Parser with Apache Airflow + Discord Integration

This project automates the extraction of the latest **Summer 2026 internship listings** from the [SimplifyJobs/Summer2026-Internships](https://github.com/SimplifyJobs/Summer2026-Internships) GitHub repository and posts them daily to a specified **Discord channel** using a webhook.

It leverages **Apache Airflow** to schedule, execute, and orchestrate tasks, and includes **GitPython**, **regex-based NLP parsing**, and **Discord webhooks** for seamless automation.

---

## 📌 Project Objectives

- ✅ Automatically clone a public GitHub repository daily  
- ✅ Parse the top internship listings from the `README.md`  
- ✅ Format the results into a concise Discord message  
- ✅ Push that message to a Discord server using a webhook  
- ✅ Handle missing data, malformed entries, and emojis

---

## 🧠 Why This Project?

Finding up-to-date internship listings often requires manual effort or constant checking of websites. This project automates that process by:

- Scraping structured data from a community-curated GitHub repository
- Eliminating noisy information (e.g., emojis, ads, banners)
- Delivering timely, clean listings directly to your Discord server

---

## ⚙️ Architecture
             +------------------------+
             |  Apache Airflow DAG    |
             +-----------+------------+
                         |
     +-------------------+------------------+
     |                                      |
+--------v--------+ +-----------v------------+
| Clone GitHub | | Parse README.md |
| Repository | | - Strip emojis |
| via GitPython | | - Extract top 10 rows |
+--------+--------+ +-----------+------------+
| |
+-------------------+------------------+
|
+----------v----------+
| Send to Discord |
| via Webhook API |
+---------------------+


---

## 🧩 Technologies Used

- **Apache Airflow** – DAG scheduling and orchestration  
- **GitPython** – Cloning and interacting with the GitHub repo  
- **Python 3.12+** – Core scripting language  
- **Discord Webhooks** – Real-time message delivery  
- **Regex** – Emoji removal and content filtering  
- **Docker** *(optional)* – For deployment and local orchestration  
- **Astronomer CLI** *(optional)* – If using Astronomer platform


---

## ⚒️ DAG Task Breakdown

```python
@dag(schedule="@daily", start_date=datetime(2025, 7, 30))
def github_readme_discord():
    clone_repo -> parse_readme -> send_to_discord

🚀 Getting Started
✅ Prerequisites
Apache Airflow set up locally or on Astronomer

Python 3.9+

A Discord server with a webhook UR

# 1. Clone this repository
git clone https://github.com/your-username/github-internship-parser.git
cd github-internship-parser

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your webhook in Airflow
airflow variables set DISCORD_WEBHOOK_URL "https://discord.com/api/webhooks/..."

# 4. Start Airflow
airflow standalone


----------
Sample Output on Discord

🚀 Top Internship Listings from SimplifyJobs:
1. EControls — IoT Software Developer Intern — San Antonio, TX
2. Tencent — Cloud Media Services Intern — Palo Alto, CA
3. CACI — Software Development Intern — Dulles, VA
...

Use Cases
CS Clubs sharing job boards automatically

Personal internship alert system

HR teams monitoring open roles

Discord bots that deliver job leads daily


🤝 Acknowledgments
Pitt CSC & Simplify for maintaining the GitHub repo

Apache Airflow for scheduling orchestration

Discord for developer-friendly webhooks



