import ipaddress
import os
from typing import List, Optional, Tuple

from src.core.path_manager import PathManager


class WindowsHostsManager:
    def __init__(self, hosts_path: Optional[str] = None):
        # Windows default; you can pass a test file path while developing
        self.hosts_path = (
            PathManager().paths.system_host
        )

    # ---------- core io ----------
    def _read_hosts(self) -> List[str]:
        if not os.path.exists(self.hosts_path):
            raise FileNotFoundError(f"Hosts file not found: {self.hosts_path}")
        with open(self.hosts_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()

    def _write_hosts_atomic(self, lines: List[str]) -> None:
        # Write atomically to reduce risk of corruption
        tmp = self.hosts_path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            # ensure every line ends with \n
            for line in lines:
                if not line.endswith("\n"):
                    line = line.rstrip("\r\n") + "\n"
                f.write(line)
        os.replace(tmp, self.hosts_path)

    # ---------- parsing helpers ----------
    @staticmethod
    def _split_comment(line: str) -> Tuple[str, str]:
        """Return (content_without_comment, comment_including_hash_or_empty)."""
        idx = line.find("#")
        if idx == -1:
            return line.rstrip("\r\n"), ""
        return line[:idx].rstrip(), line[idx:].rstrip("\r\n")

    @staticmethod
    def _parse_mapping(line: str):
        """
        Parse a hosts mapping line.
        Returns (leading_ws, ip, hostnames_list, comment) or None if not a mapping.
        """
        content, comment = WindowsHostsManager._split_comment(line)
        if not content.strip():
            return None  # blank or comment-only

        # preserve leading whitespace for nicer rewrites
        leading_len = len(content) - len(content.lstrip())
        leading_ws = content[:leading_len]
        body = content.strip()
        parts = body.split()
        if not parts:
            return None

        ip_token = parts[0]
        try:
            ipaddress.ip_address(ip_token)
        except ValueError:
            return None  # not a valid IP -> not a mapping line

        hostnames = parts[1:]
        return leading_ws, ip_token, hostnames, comment

    @staticmethod
    def _build_line(leading_ws: str, ip: str, hostnames: List[str], comment: str) -> str:
        base = f"{leading_ws}{ip}\t{' '.join(hostnames)}" if hostnames else f"{leading_ws}{ip}"
        if comment:
            # ensure a single space before comment
            if not comment.startswith("#"):
                comment = "#" + comment
            base += " " + comment
        return base + "\n"

    @staticmethod
    def _norm(host: str) -> str:
        return host.strip().lower()

    # ---------- public api ----------
    def add_entry(self, domain: str, ip="127.0.0.1") -> bool:
        """
        Idempotent add:
        - True if added or already exists
        - False on failure
        """
        try:
            ipaddress.ip_address(ip)  # validate ip
            target = self._norm(domain)

            lines = self._read_hosts()
            # Check if mapping already present (domain present on a line with same IP)
            for line in lines:
                parsed = self._parse_mapping(line)
                if not parsed:
                    continue
                _, ip_token, hosts, _ = parsed
                if ip_token == ip and any(self._norm(h) == target for h in hosts):
                    return True  # already present

            # Not present -> append a clean line
            lines.append(f"{ip}\t{domain}\n")
            self._write_hosts_atomic(lines)
            return True
        except Exception as e:
            print(f"[!] Error while adding entry: {e}")
            return False

    def delete_entry(self, domain: str, ip: Optional[str] = None) -> bool:
        """
        Delete entries:
        - If ip is None: remove 'domain' from ANY IP lines (all copies).
        - If ip is given: remove 'domain' only from lines with that IP (all copies).

        Returns True on success (even if nothing to remove), False on failure.
        """
        try:
            target = self._norm(domain)
            if ip is not None:
                # validate IP if provided
                ipaddress.ip_address(ip)

            lines = self._read_hosts()
            new_lines: List[str] = []
            changed = False

            for line in lines:
                parsed = self._parse_mapping(line)
                if not parsed:
                    new_lines.append(line)
                    continue

                leading_ws, ip_token, hosts, comment = parsed

                # decide if this line is affected
                if ip is not None and ip_token != ip:
                    # specific IP requested and this isn't it -> keep as is
                    new_lines.append(line)
                    continue

                # remove the target domain (case-insensitive) from this mapping
                kept_hosts = [h for h in hosts if self._norm(h) != target]

                if len(kept_hosts) != len(hosts):
                    changed = True
                    if kept_hosts:
                        # keep the line but without the removed host
                        new_lines.append(self._build_line(leading_ws, ip_token, kept_hosts, comment))
                    else:
                        # no hostnames left -> drop the entire line
                        # (comment is dropped as it belonged to this mapping)
                        pass
                else:
                    # nothing to remove on this line
                    new_lines.append(line)

            if changed:
                self._write_hosts_atomic(new_lines)
            return True
        except Exception as e:
            print(f"[!] Error while deleting entry: {e}")
            return False


if __name__ == "__main__":
    # Example usage
    mgr = WindowsHostsManager()
    # Add
    print("ADD:", mgr.add_entry("127.0.0.1", "example.local"))
    # Delete only that mapping
    print("DEL exact:", mgr.delete_entry("example.local", ip="127.0.0.1"))
    # Delete by domain across any IPs
    print("DEL any-ip:", mgr.delete_entry("example.local"))
