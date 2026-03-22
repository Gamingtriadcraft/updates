import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from version import get_version
from updates.updater import GitHubUpdater
import time

def main():
    print(f"App Version: {get_version()}")
    print("-" * 50)
    
    # IMPORTANT: Replace these with your actual GitHub username and repo name
    updater = GitHubUpdater(
        repo_owner="Gamingtriadcraft",  # Change this!
        repo_name="updates",         # Change this!
        current_version=get_version(),
        branch="main"
    )
    
    print("Checking for updates...")
    update_info = updater.check_for_updates()
    
    if update_info.get("error"):
        print(f"Error: {update_info['error']}")
        print("This is normal if you haven't pushed to GitHub yet.")
    elif update_info.get("update_available"):
        print(f"Update available: {update_info['latest_version']}")
    else:
        print(f"You're up to date!")
    
    print("\nRunning app... (Press Ctrl+C to stop)")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
