# My App with Auto-Update

A Python application with GitHub-based auto-update functionality.

## Features

- Auto-checks for updates from GitHub
- Downloads updates in background
- Version management with rollback support
- No forced updates - users update when ready

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python app/main.py
```

## Updating

To push a new version:
```bash
# 1. Update version.py
# 2. Update manifest
python scripts/update_manifest.py 1.1.0 YOUR_USERNAME YOUR_REPO "New features"

# 3. Commit and tag
git add .
git commit -m "Release v1.1.0"
git tag v1.1.0
git push origin main --tags
```

## Version

Current version: 1.0.0
