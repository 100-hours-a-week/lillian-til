import os
import shutil
import datetime
import subprocess

# Get the current date
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
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

# Add, commit, and push changes to GitHub
try:
    subprocess.run(["git", "add", "-f", new_file_path], check=True)
    subprocess.run(["git", "commit", "-m", f"Auto-copied template.md to {month_folder}/{date_str}.md"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("Changes pushed to GitHub successfully.")
except subprocess.CalledProcessError as e:
    print(f"Git error: {e}")
