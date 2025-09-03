import os
import shutil
import subprocess
import zipfile

from colorama import Fore


class Extractor:
    def __init__(self, seven_zip_path="7z"):
        """
        :param seven_zip_path: Path to 7z binary (default assumes '7z' is in PATH)
        """
        # self.binaries = binaries
        self.seven_zip_path = seven_zip_path
        self.seven_zip_available = shutil.which(seven_zip_path) is not None

    def extract(self, src_file: str, target_dir: str):
        """Extracts a given archive file into a target directory using 7-Zip or fallback extractor."""
        os.makedirs(target_dir, exist_ok=True)
        print(Fore.GREEN + f"Extracting {os.path.basename(src_file)} -> {target_dir}")

        if self.seven_zip_available:
            return self._extract_with_7z(src_file, target_dir)
        else:
            return self._extract_with_windows(src_file, target_dir)

    def _extract_with_7z(self, src_file: str, target_dir: str):
        """Try extracting using 7-Zip."""
        cmd = f'"{self.seven_zip_path}" x "{src_file}" -y -o"{target_dir}"'
        try:
            result = subprocess.run(
                cmd, shell=True, check=True, capture_output=True, text=True
            )
            print(Fore.CYAN + f"✔ Done (7-Zip): {os.path.basename(src_file)}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"❌ 7-Zip failed: {e.stderr}")
            raise

    def _extract_with_windows(self, src_file: str, target_dir: str):
        """Fallback: Extract using Windows native extractor (ZIP only)."""
        if not src_file.lower().endswith(".zip"):
            print(Fore.RED + "❌ Only .zip supported in Windows fallback extractor")
            raise RuntimeError("Unsupported archive type without 7-Zip")

        try:
            with zipfile.ZipFile(src_file, "r") as zip_ref:
                zip_ref.extractall(target_dir)
            print(Fore.CYAN + f"✔ Done (Windows Native): {os.path.basename(src_file)}")
            return f"Extracted {src_file} using Windows native ZIP support"
        except Exception as e:
            print(Fore.RED + f"❌ Windows extractor failed: {e}")
            raise
