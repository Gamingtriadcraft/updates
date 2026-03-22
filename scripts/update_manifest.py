import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime


def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def update_manifest(version, repo_owner, repo_name, changes=None):
    """Update version manifest with new release"""
    manifest_path = Path("updates") / "version_manifest.json"
    
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    else:
        manifest = {
            "latest_version": version,
            "min_supported_version": version,
            "versions": {},
            "deprecated_versions": []
        }
    
    files_to_track = [
        "app/core/processor.py",
        "app/main.py",
    ]
    
    version_info = {
        "released": datetime.now().strftime("%Y-%m-%d"),
        "changes": changes or [f"Release {version}"],
        "files": {},
        "required_update": False
    }
    
    for file_path in files_to_track:
        file_obj = Path(file_path)
        if file_obj.exists():
            sha256 = calculate_sha256(file_path)
            version_info["files"][file_path] = {
                "sha256": sha256,
                "url": f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/v{version}/{file_path}"
            }
            print(f"✓ Tracked: {file_path}")
    
    manifest["latest_version"] = version
    manifest["versions"][version] = version_info
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✓ Updated manifest for version {version}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python scripts/update_manifest.py <version> <github_username> <repo_name> [changes...]")
        sys.exit(1)
    
    version = sys.argv[1]
    repo_owner = sys.argv[2]
    repo_name = sys.argv[3]
    changes = sys.argv[4:] if len(sys.argv) > 4 else None
    
    update_manifest(version, repo_owner, repo_name, changes)
