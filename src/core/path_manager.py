from pathlib import Path

from src.core.binaries import Binaries
from src.core.constants import Constants
from src.core.system_paths import SystemPaths


class PathManager:
    def __init__(self):
        # Discover project root dynamically
        self._project_root = Path(__file__).resolve().parents[2]
        self._install_drive = Path(SystemPaths().system_drive)
        self._deployment_root = self._install_drive / Constants.BRAND_NAME

        # --- Project paths ---
        self._project = {
            Constants.KEY_ROOT: self._project_root,
            "prerequisite": self._project_root / "src" / "prerequisite",
            "templates": self._project_root / "src" / "includes" / "templates",
        }

        # --- Deployment structure ---
        apache_file = Binaries().get()[Constants.DIR_APACHE].get("file")
        apache_root = (
                self._deployment_root
                / Constants.DIR_BIN
                / Constants.DIR_APACHE
                / Path(apache_file).stem
                / "Apache24"
        )

        php_file = Binaries().get()[Constants.DIR_PHP].get("file")
        php_root = (
                self._deployment_root
                / Constants.DIR_BIN
                / Constants.DIR_PHP
                / Path(php_file).stem
        )

        self._structure = {
            Constants.KEY_ROOT: self._deployment_root,
            Constants.DIR_BIN: self._deployment_root / Constants.DIR_BIN,
            Constants.DIR_TEMP: self._deployment_root / Constants.DIR_TEMP,
            Constants.DIR_WWW: self._deployment_root / Constants.DIR_WWW,
            Constants.DIR_COMMAND: self._deployment_root / Constants.DIR_COMMAND,

            # Apache related
            "apache_root": apache_root,
            "httpd_exe": apache_root / "bin" / "httpd.exe",
            "httpd_conf": apache_root / "conf" / "httpd.conf",
            "httpd_vhost_conf": apache_root / "conf" / "extra" / "httpd-vhosts.conf",

            # PHP related
            "php_root": php_root,
            "php_ini": php_root / "php.ini",
            # Project deployment entry
            "index": self._deployment_root / "www" / "index.php",
        }

    # -----------------------
    # Public API
    # -----------------------
    def deploy_root(self) -> Path:
        return self._structure[Constants.KEY_ROOT]

    def deploy_structure(self, key: str) -> str:
        try:
            return str(self._structure[key])
        except KeyError:
            raise RuntimeError(f"Unknown deployment structure key: {key}")

    def project_structure(self, key: str) -> str:
        try:
            return str(self._project[key])
        except KeyError:
            raise RuntimeError(f"Unknown project structure key: {key}")

    @property
    def paths(self) -> SystemPaths:
        return SystemPaths()

    @property
    def system_drive(self) -> Path:
        return Path(SystemPaths().system_drive)

    @property
    def program_files(self) -> Path:
        return Path(SystemPaths().program_files)
