import os
import platform
import sys
import tempfile
from pathlib import Path


class SystemPaths:
    def __init__(self):
        if platform.system() != "Windows":
            raise OSError("SystemPaths (Windows) can only run on Windows")

        self.platform = platform.system()  # "Windows"
        self.arch = platform.machine()  # "AMD64" or "ARM64"
        self.python_exec = sys.executable  # Python executable path

    @property
    def cwd(self) -> str:
        """Current working directory"""
        return os.getcwd()

    @property
    def home(self) -> str:
        """User home directory (C:\\Users\\Name)"""
        return str(Path.home())

    @property
    def desktop(self) -> str:
        """User Desktop folder"""
        return str(Path.home() / "Desktop")

    @property
    def documents(self) -> str:
        """User Documents folder"""
        return str(Path.home() / "Documents")

    @property
    def downloads(self) -> str:
        """User Downloads folder"""
        return str(Path.home() / "Downloads")

    @property
    def appdata(self) -> str:
        """Roaming AppData folder (C:\\Users\\Name\\AppData\\Roaming)"""
        return os.environ.get("APPDATA", "")

    @property
    def local_appdata(self) -> str:
        """Local AppData folder (C:\\Users\\Name\\AppData\\Local)"""
        return os.environ.get("LOCALAPPDATA", "")

    @property
    def program_files(self) -> str:
        """Program Files (C:\\Program Files)"""
        return os.environ.get("ProgramFiles", "")

    @property
    def program_files_x86(self) -> str:
        """Program Files (x86)"""
        return os.environ.get("ProgramFiles(x86)", "")

    @property
    def temp(self) -> str:
        """System temp directory"""
        return tempfile.gettempdir()

    @property
    def system_drive(self) -> str:
        """System drive root (Windows: C:, Linux/Mac: /)"""
        if "windows" in self.platform.lower():
            return os.environ.get("SystemDrive", "C:") + "\\"  # usually C:
        else:
            return "/"  # root filesystem for Unix-like systems

    @property
    def system_host(self) -> str:
        """System hostname"""
        return self.system_drive + os.path.join(
            "Windows", "System32", "drivers", "etc", "hosts"
        )

    @property
    def script_path(self) -> str:
        """Path of the currently running script"""
        return os.path.abspath(sys.argv[0])

    def join(self, *parts) -> str:
        """Cross-platform safe path join"""
        return os.path.join(*parts)

    def exists(self, path) -> bool:
        """Check if path exists"""
        return os.path.exists(path)

    def mkdir(self, path, parents=True, exist_ok=True):
        """Create directories safely"""
        Path(path).mkdir(parents=parents, exist_ok=exist_ok)
        return path
