import os
import winreg


class EnvPathManager:
    SYSTEM_REQUIRED_PATHS = {
        r"C:\Windows",
        r"C:\Windows\System32",
        r"C:\Windows\System32\Wbem",
        r"C:\Windows\System32\WindowsPowerShell\v1.0",
    }

    CUSTOM_MARKER = "#CUSTOM_PATH#"  # marker to track our custom entry

    def __init__(self, system=True):
        """
        system=True  -> System PATH (all users, requires admin)
        system=False -> User PATH (current user only)
        """
        self.var_name = "Path"
        if system:
            self.scope = winreg.HKEY_LOCAL_MACHINE
            self.subkey = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        else:
            self.scope = winreg.HKEY_CURRENT_USER
            self.subkey = r"Environment"

    def _read(self):
        with winreg.OpenKey(self.scope, self.subkey, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, self.var_name)
            return value.split(";")

    def _write(self, paths):
        """Write back into registry permanently"""
        # Remove duplicates and empties
        final_paths = []
        seen = set()
        for p in paths:
            if p and p not in seen:
                final_paths.append(p)
                seen.add(p)

        value = ";".join(final_paths)

        with winreg.OpenKey(self.scope, self.subkey, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, self.var_name, 0, winreg.REG_EXPAND_SZ, value)

        # Apply changes to current session
        os.system("setx PATH \"" + value + "\" " + ("/M" if self.scope == winreg.HKEY_LOCAL_MACHINE else ""))

    def list(self):
        return self._read()

    def add(self, new_path):
        """
        Add/replace a single custom path without deleting others.
        Keeps all existing user-defined entries.
        """
        paths = self._read()

        # Remove old custom entry if exists
        paths = [p for p in paths if not p.endswith(self.CUSTOM_MARKER)]

        # Add new custom with marker
        paths.append(new_path)

        self._write(paths)

    def delete(self, target_path):
        """Delete only if it's not required"""
        paths = self._read()
        new_paths = []
        for p in paths:
            raw_p = p.replace(self.CUSTOM_MARKER, "")
            if raw_p == target_path and raw_p not in self.SYSTEM_REQUIRED_PATHS:
                continue
            new_paths.append(p)
        self._write(new_paths)

    def sort_by_length(self):
        paths = self._read()
        req = [p for p in paths if p in self.SYSTEM_REQUIRED_PATHS]
        others = [p for p in paths if p not in self.SYSTEM_REQUIRED_PATHS]
        self._write(req + sorted(others, key=lambda x: len(x.replace(self.CUSTOM_MARKER, ""))))

    def sort_by_alphabet(self):
        paths = self._read()
        req = [p for p in paths if p in self.SYSTEM_REQUIRED_PATHS]
        others = [p for p in paths if p not in self.SYSTEM_REQUIRED_PATHS]
        self._write(req + sorted(others, key=lambda x: x.replace(self.CUSTOM_MARKER, "")))
