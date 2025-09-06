import glob
import os
import re
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

from colorama import Fore

# local imports (unchanged)
from src.core.certificate_manager import CertificateManager
from src.core.cli_arguments import Arguments
from src.core.constants import Constants
from src.core.helper import Helper
from src.core.path_manager import PathManager
from src.core.service import Service
from src.core.system_paths import SystemPaths
from src.core.windows_host_manager import WindowsHostsManager


class VirtualHost:
    """
    Manage Apache virtual host configs and Windows hosts entries.

    Notes:
    - Editing apache vhost file requires appropriate permissions (run as admin if necessary).
    - Updating hosts file requires Administrator privileges.
    """

    def __init__(self):
        # instantiate system paths at runtime (avoid import-time side effects)
        self._system_paths = SystemPaths()
        self.HOSTS_FILE = self._system_paths.system_host  # path to hosts file

        self.path_manager = PathManager()
        # use constant key used in your codebase
        self.apache_v_host = self.path_manager.deploy_structure("httpd_vhost_conf")
        if not os.path.exists(self.apache_v_host):
            raise FileNotFoundError(f"Apache vhost config not found: {self.apache_v_host}")

    # -------------------------
    # Public operations
    # -------------------------
    def add(
            self,
            hostname: str,
            port: int,
            app_root: str,
            ssl: bool = False,
            balancer: bool = False,
            members: Optional[Iterable[str]] = None,
    ):
        """Add a virtual host + hosts entry. Creates certs if ssl=True."""
        hostname = (hostname or "").strip()
        if not hostname:
            raise ValueError("hostname must be provided")

        if self._vhost_exists(hostname):
            print(f"{Fore.YELLOW}Warning: requested hostname {hostname} already exits")
            exit(1)
            # raise RuntimeError(f"VirtualHost for '{hostname}' already exists in {self.apache_v_host}")

        # ensure port is int
        try:
            port = int(port)
        except (TypeError, ValueError):
            raise ValueError("port must be an integer")

        # ensure app_root exists (or warn)
        if not os.path.isdir(app_root):
            # try to create directory
            try:
                Path(app_root).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise RuntimeError(f"Project root '{app_root}' missing and could not be created: {e}")

        # 1. SSL certs
        if ssl:
            try:
                CertificateManager.create(self.apache_v_host, hostname)
            except Exception as e:
                raise RuntimeError(f"Failed to create certificate for {hostname}: {e}")

        # 2. Build config
        if balancer:
            cfg = self.build_balancer(hostname, port, members or [], ssl=ssl)
        else:
            cfg = self.build(hostname, port, app_root, ssl=ssl)

        # 3. Append config safely with backup
        self._backup_config()
        try:
            with open(self.apache_v_host, "a", encoding="utf-8", newline="\n") as f:
                f.write("\n")
                f.write(cfg)
                f.write("\n")
        except PermissionError as e:
            raise PermissionError(f"Permission denied writing to {self.apache_v_host}: {e}")

        # 4. Update hosts file
        try:
            WindowsHostsManager().add_entry(hostname)
        except Exception as e:
            # hosts update failed - warn (vhost added) but keep file as is
            print(f"{Fore.YELLOW}Warning: failed to update hosts file for {hostname}: {e}")

        print(f"{Fore.GREEN}Virtual Host added for {Fore.CYAN}{hostname}")

    def remove(self, hostname: str):
        """Remove virtualhost blocks containing ServerName <hostname> and update hosts."""
        hostname = (hostname or "").strip()
        if not hostname:
            raise ValueError("hostname must be provided")

        # read file
        p = Path(self.apache_v_host)
        text = p.read_text(encoding="utf-8")

        # Regex to find <VirtualHost ...> ... </VirtualHost> blocks (non-greedy),
        # and remove those that contain ServerName <hostname>
        pattern = re.compile(
            r"(<VirtualHost\b.*?>.*?</VirtualHost>)", re.IGNORECASE | re.DOTALL
        )

        def keep_block(m):
            block = m.group(1)
            # if ServerName hostname present in block -> remove it
            if re.search(rf"^\s*ServerName\s+{re.escape(hostname)}\b", block, re.IGNORECASE | re.MULTILINE):
                return ""  # delete block
            # also check for ServerAlias entries (safer)
            if re.search(rf"^\s*ServerAlias\s+.*\b{re.escape(hostname)}\b", block, re.IGNORECASE | re.MULTILINE):
                return ""
            return block  # keep

        new_text = pattern.sub(lambda m: keep_block(m), text)

        if new_text == text:
            print(f"{Fore.YELLOW}Note: No VirtualHost block found for {hostname} in {self.apache_v_host}")
        else:
            # backup then write
            backup_file = self._backup_config()
            try:
                p.write_text(new_text, encoding="utf-8", newline="\n")
            except PermissionError as e:
                raise PermissionError(f"Permission denied writing to {self.apache_v_host}: {e}")

            # remove hosts entry
            try:
                WindowsHostsManager().delete_entry(hostname)
            except Exception as e:
                print(f"{Fore.YELLOW}Warning: failed to remove hosts entry for {hostname}: {e}")

            print(f"{Fore.GREEN}Virtual Host removed for {Fore.CYAN}{hostname}")

    # -------------------------
    # CLI-friendly wrappers
    # -------------------------
    def add_project(self, args: Arguments):
        try:
            hostname = args.get("hostname")
            if not hostname:
                raise RuntimeError("Wrong hostname provided")

            root_dir = args.get("dir", self.path_manager.deploy_structure(Constants.DIR_WWW))
            if not root_dir:
                raise RuntimeError("Wrong project directory")

            port = args.get("port", 80)
            ssl = args.get("ssl", False)
            balancer = args.get("balancer", False)
            members = args.get("members", None)

            self.add(hostname, port, root_dir, ssl=ssl, balancer=balancer, members=members)
            Service().restart()
            Helper.open_app(hostname, port, ssl)
        finally:
            self.__cleanup_backups()

    def remove_project(self, args: Arguments):
        try:
            hostname = args.get("hostname")
            if not hostname:
                raise RuntimeError("Wrong hostname provided")
            self.remove(hostname)
            Service().restart()
        finally:
            self.__cleanup_backups()

    # -------------------------
    # Build helpers
    # -------------------------
    @staticmethod
    def build(hostname: str, port: int, app_root: str, ssl: bool = False) -> str:
        """Return a demented Apache VirtualHost block."""
        ssl_block = ""
        if ssl:
            ssl_block = textwrap.dedent(
                f"""
            SSLEngine on
            SSLCertificateKeyFile "cert/{hostname}.key"
            SSLCertificateFile "cert/{hostname}.crt"
            """
            )

        template = f"""
    <VirtualHost *:{port}>
        DocumentRoot "{app_root}"
        ServerName {hostname}
        ErrorLog "logs/{hostname}-error.log"
        CustomLog "logs/{hostname}-access.log" common
        <Directory "{app_root}">
            AllowOverride All
            Require all granted
        </Directory>{ssl_block}
    </VirtualHost>
    """
        return textwrap.dedent(template).strip() + "\n"

    @staticmethod
    def build_balancer(hostname: str, port: int, members: Iterable[str], ssl: bool = False) -> str:
        members = list(members or [])
        balancer_members = "\n".join([f"        BalancerMember {m}" for m in members])
        template = f"""
    <VirtualHost *:{port}>
        ProxyRequests Off
        ProxyPass / balancer://{hostname}_cluster/
        <Proxy balancer://{hostname}_cluster>
    {balancer_members}
        </Proxy>
    </VirtualHost>
    """
        return textwrap.dedent(template).strip() + "\n"

    # -------------------------
    # Utilities
    # -------------------------
    def _vhost_exists(self, hostname: str) -> bool:
        """Quick check if a ServerName or ServerAlias matches hostname in config file."""
        text = Path(self.apache_v_host).read_text(encoding="utf-8")
        if re.search(rf"^\s*ServerName\s+{re.escape(hostname)}\b", text, re.IGNORECASE | re.MULTILINE):
            return True
        if re.search(rf"^\s*ServerAlias\s+.*\b{re.escape(hostname)}\b", text, re.IGNORECASE | re.MULTILINE):
            return True
        return False

    def _backup_config(self):
        """Create a timestamped backup of the vhost config before modification."""
        src = Path(self.apache_v_host)
        if not src.exists():
            return
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        dest = src.with_name(f"{src.name}.bak.{ts}")
        try:
            dest.write_bytes(src.read_bytes())
            print(f"[backup] {src} -> {dest}")
            return dest
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: failed to create backup of {src}: {e}")

    @staticmethod
    def __cleanup_backups():
        """Remove leftover .bak timestamped backup files after successful operations"""
        base_paths = [
            # SystemPaths().system_host,  # hosts file
            PathManager().deploy_structure('httpd_vhost_conf'),  # apache vhost conf
        ]

        patterns = []
        for path in base_paths:
            patterns.append(path + ".bak*")  # match .bak, .bak.timestamp, etc.

        # certificates: cert/{hostname}.crt.bak.2025..., cert/{hostname}.key.bak.2025...
        # patterns.append(os.path.join("cert", "*.bak*"))

        for pattern in patterns:
            for bak in glob.glob(pattern):
                try:
                    os.remove(bak)
                    # print(f"Removed backup: {bak}")
                except Exception as e:
                    print(f"Warning: could not remove {bak}: {e}")
