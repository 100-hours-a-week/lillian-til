import os
import shutil
import datetime
import subprocess

# Get today's date
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")  # Format: 2025-02-07
title = today.strftime("%y.%m.%d")  # Format: 25.02.07
month_folder = today.strftime("%m-%b")  # Format: 02-Feb

# Stop creating files after July
if today.month > 7:
    print(f"Skipping file creation since month is after July ({month_folder}).")
    exit()

# Define file paths
repo_root = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
template_file = os.path.join(repo_root, "template.md")
month_dir = os.path.join(repo_root, month_folder)
new_file_path = os.path.join(month_dir, f"{date_str}.md")
readme_path = os.path.join(repo_root, "README.md")

# Ensure the script runs inside a Git repository
if not os.path.exists(os.path.join(repo_root, ".git")):
    print("Error: This script must be placed inside a Git repository.")
    exit(1)

# Fetch the latest changes from GitHub
try:
    print("Fetching latest updates from GitHub...")
    subprocess.run(["git", "fetch", "origin"], check=True)
    subprocess.run(["git", "pull", "origin", "main"], check=True)  # Change "main" to your default branch if needed
    print("Repository is up to date.")
except subprocess.CalledProcessError as e:
    print(f"Git fetch/pull error: {e}")
    exit(1)

# Ensure the month folder exists
os.makedirs(month_dir, exist_ok=True)

# Copy and rename the template file
if os.path.exists(template_file):
    shutil.copy(template_file, new_file_path)
    print(f"Copied {template_file} to {new_file_path}")
else:
    print("Error: template.md not found!")
    exit(1)

# Read existing README.md content
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as file:
        readme_lines = file.readlines()
else:
    readme_lines = []

# Determine the start of the current week (Monday)
monday_start = today - datetime.timedelta(days=today.weekday())  # Move to Monday of the current week

# Find the first Monday of the month
first_monday = today.replace(day=1)
while first_monday.weekday() != 0:  # Find the first Monday of the month
    first_monday += datetime.timedelta(days=1)

# Calculate the current week number in the month (starting from Monday)
week_of_month = ((monday_start - first_monday).days // 7) + 1  # 1-based week number
korean_week_names = ["첫째주", "둘째주", "셋째주", "넷째주", "다섯째주"]
korean_week_of_month = korean_week_names[week_of_month - 1]

# Check the latest existing week section in README
last_week_number = 1
header_index = None
for index, line in enumerate(readme_lines):
    if line.startswith("### ["):
        parts = line.split()
        if len(parts) >= 3:
            try:
                last_week_number = int(parts[2][0])  # Extract cumulative week number
                header_index = index
            except ValueError:
                continue

# **FIXED: Correct week number calculation**
iso_year, iso_week, _ = today.isocalendar()  # Get ISO year, week, and weekday
recording_week_number = max(iso_week - 4, 1)  # Adjust to "week of year - 4" (ensuring it doesn’t go below 1)

# Add new week section in README on Mondays
if today.weekday() == 0 and last_week_number < week_of_month:
    week_header = f"\n### [{today.month}월 {korean_week_of_month}, {recording_week_number}주차] : 간략 주제 작성\n\n"
    readme_lines.append(week_header)

# Append new daily entry
new_readme_entry = f"\n[{title}](https://github.com/100-hours-a-week/lillian-til/blob/main/{month_folder}/{date_str}.md) 세부 주제 1 작성\n\n"
readme_lines.append(new_readme_entry)

# Write updated README.md
with open(readme_path, "w", encoding="utf-8") as file:
    file.writelines(readme_lines)

print(f"Updated {readme_path} with new entry.")

# Add, commit, and push changes to GitHub
try:
    subprocess.run(["git", "add", "-f", new_file_path, readme_path], check=True)
    subprocess.run(["git", "commit", "-m", f"Updated README and added {month_folder}/{date_str}.md"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("Changes pushed to GitHub successfully.")
except subprocess.CalledProcessError as e:
    print(f"Git error: {e}")