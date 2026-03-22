import requests
import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, List
from packaging import version as pkg_version
import shutil
import tempfile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitHubUpdater:
    def __init__(
        self,
        repo_owner: str,
        repo_name: str,
        current_version: str,
        branch: str = "main",
        cache_dir: Optional[Path] = None
    ):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.branch = branch
        
        self.cache_dir = cache_dir or Path.home() / ".myapp" / "updates"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.base_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}"
        self.manifest_url = f"{self.base_url}/updates/version_manifest.json"
    
    def check_for_updates(self) -> Dict:
        try:
            response = requests.get(self.manifest_url, timeout=10)
            response.raise_for_status()
            manifest = response.json()
            
            latest = manifest.get("latest_version", self.current_version)
            min_supported = manifest.get("min_supported_version", "0.0.0")
            
            current_v = pkg_version.parse(self.current_version)
            latest_v = pkg_version.parse(latest)
            min_v = pkg_version.parse(min_supported)
            
            return {
                "update_available": current_v < latest_v,
                "latest_version": latest,
                "current_version": self.current_version,
                "update_required": current_v < min_v,
                "min_supported_version": min_supported,
                "deprecated": self.current_version in manifest.get("deprecated_versions", []),
                "manifest": manifest
            }
        except Exception as e:
            logger.error(f"Failed to check for updates: {e}")
            return {
                "update_available": False,
                "error": str(e),
                "current_version": self.current_version
            }
    
    def download_update(self, target_version: str) -> bool:
        try:
            response = requests.get(self.manifest_url, timeout=10)
            manifest = response.json()
            
            if target_version not in manifest.get("versions", {}):
                logger.error(f"Version {target_version} not found in manifest")
                return False
            
            version_info = manifest["versions"][target_version]
            files = version_info.get("files", {})
            
            temp_dir = Path(tempfile.mkdtemp())
            
            try:
                for file_path, file_info in files.items():
                    success = self._download_file(
                        file_info["url"],
                        temp_dir / file_path,
                        file_info.get("sha256")
                    )
                    if not success:
                        logger.error(f"Failed to download {file_path}")
                        return False
                
                version_cache = self.cache_dir / target_version
                if version_cache.exists():
                    shutil.rmtree(version_cache)
                
                shutil.move(str(temp_dir), str(version_cache))
                logger.info(f"Successfully downloaded version {target_version}")
                return True
                
            finally:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
        
        except Exception as e:
            logger.error(f"Failed to download update: {e}")
            return False
    
    def _download_file(self, url: str, dest_path: Path, expected_sha256: Optional[str] = None) -> bool:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            content = response.content
            
            if expected_sha256:
                actual_sha256 = hashlib.sha256(content).hexdigest()
                if actual_sha256 != expected_sha256:
                    logger.error(f"Checksum mismatch for {dest_path}")
                    return False
            
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_bytes(content)
            return True
            
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            return False
