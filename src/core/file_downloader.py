import os
import shutil
import subprocess

import requests
from tqdm import tqdm  # progress bar


class FileDownloader:
    def __init__(self, target_folder="downloads"):
        """Initialize downloader with a target folder."""
        self.target_folder = os.path.abspath(target_folder)
        os.makedirs(self.target_folder, exist_ok=True)

    def _run_command(self, command):
        """Helper: Run a shell command safely."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _download_with_curl(self, url, filepath):
        return self._run_command(f'curl -L -o "{filepath}" "{url}"')

    def _download_with_powershell(self, url, filepath):
        return self._run_command(
            f"powershell -Command \"Invoke-WebRequest -Uri '{url}' -OutFile '{filepath}'\""
        )

    def _download_with_wget(self, url, filepath):
        return self._run_command(f'wget -O "{filepath}" "{url}"')

    def _download_with_requests(self, url, filepath):
        try:
            with requests.get(
                    url, stream=True, timeout=60, proxies={"http": None, "https": None}
            ) as resp:
                resp.raise_for_status()
                total = int(resp.headers.get("content-length", 0))
                with (
                    open(filepath, "wb") as f,
                    tqdm(
                        total=total,
                        unit="B",
                        unit_scale=True,
                        desc=os.path.basename(filepath),
                    ) as bar,
                ):
                    for chunk in resp.iter_content(8192):
                        f.write(chunk)
                        bar.update(len(chunk))
            return True
        except Exception as e:
            print(f"❌ Python requests failed: {e}")
            return False

    def download(self, url, filename=None):
        """Download a file using curl, PowerShell, wget, or requests."""
        if not filename:
            filename = os.path.basename(url.split("?")[0]) or "download.tmp"

        filepath = os.path.join(self.target_folder, filename)

        print(f"\n⬇️  Downloading {url}\n   → {filepath}")

        # Strategy 1: curl
        if shutil.which("curl") and self._download_with_curl(url, filepath):
            print("✅ Downloaded with curl")
            return filepath

        # Strategy 2: PowerShell (Windows only)
        if os.name == "nt" and self._download_with_powershell(url, filepath):
            print("✅ Downloaded with PowerShell")
            return filepath

        # Strategy 3: wget
        if shutil.which("wget") and self._download_with_wget(url, filepath):
            print("✅ Downloaded with wget")
            return filepath

        # Strategy 4: Python requests
        if self._download_with_requests(url, filepath):
            print("✅ Downloaded with Python requests")
            return filepath

        raise RuntimeError("❌ All download methods failed!")


# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    url = "https://www.apachelounge.com/download/VS17/binaries/httpd-2.4.65-250724-Win64-VS17.zip"
    downloader = Downloader("my_downloads")
    try:
        file_path = downloader.download(url)
        print(f"\n🎉 File saved at: {file_path}")
    except Exception as e:
        print(f"\n🚨 Download failed: {e}")
