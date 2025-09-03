import os
import subprocess

import psutil
from colorama import init, Fore

from src.core.constants import Constants
from src.core.helper import Helper
from src.core.path_manager import PathManager

# from src.core.path_manager import PathManager

init(autoreset=True)


class Service:
    RUNNING = "running"
    STOPPED = "stopped"

    def __init__(self):
        self.path_manager = PathManager()
        self.utils = Helper()

    # ------------------------
    # Public Methods
    # ------------------------
    def install(self):
        self.__service_install()

    def remove(self):
        self.stop()  # safer than direct call
        self.__service_remove()

    def start(self):
        self.__service_on_off("start")

    def stop(self):
        self.__service_on_off("stop")

    def restart(self):
        self.stop()
        self.start()

    @staticmethod
    def get(service_name: str):
        """Return service info dict if available, else None."""
        try:
            service = psutil.win_service_get(service_name)
            return service.as_dict()
        except psutil.NoSuchProcess:
            print(Fore.YELLOW + f"ℹ Service {service_name} not found.")
        except psutil.AccessDenied:
            print(Fore.RED + f"❌ Access denied while fetching {service_name} status.")
        return None

    # ------------------------
    # Private Helpers
    # ------------------------
    @staticmethod
    def __run_command(cmd: str) -> bool:
        """Run a system command safely with error handling."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            print(Fore.GREEN + f"✔ Command succeeded: {cmd}")
            if result.stdout.strip():
                print(Fore.CYAN + result.stdout.strip())
            return True
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"❌ Command failed: {cmd}")
            if e.stderr.strip():
                print(Fore.YELLOW + e.stderr.strip())
            return False
        except Exception as e:
            print(Fore.RED + f"❌ Unexpected error running command: {cmd}")
            print(Fore.YELLOW + str(e))
            return False

    def __service_install(self):
        """Install Apache as a Windows service."""
        exe = self.path_manager.deploy_structure("httpd_exe")
        if not exe or not os.path.exists(exe):
            print(Fore.RED + "❌ Apache executable not found. Cannot install service.")
            return

        cmd = f'"{exe}" -k install -n "{Constants.SERVICE_NAME_APACHE}"'
        if not self.__run_command(cmd):
            print(
                f"{Fore.RED}Error: {Fore.LIGHTYELLOW_EX}{Constants.SERVICE_NAME_APACHE}"
                f"{Fore.RED} service could not be installed."
            )

    def __service_remove(self):
        """Remove Apache service if it exists."""
        service = self.get(Constants.SERVICE_NAME_APACHE)
        if not service:
            print(Fore.YELLOW + f"ℹ Service {Constants.SERVICE_NAME_APACHE} not found.")
            return

        exe = self.path_manager.deploy_structure("httpd_exe")
        cmd = f'"{exe}" -k uninstall -n "{Constants.SERVICE_NAME_APACHE}"'
        if not self.__run_command(cmd):
            print(
                f"{Fore.RED}Error: {Fore.LIGHTYELLOW_EX}{Constants.SERVICE_NAME_APACHE}"
                f"{Fore.RED} service could not be uninstalled."
            )

    def __service_on_off(self, mode: str):
        """Start or stop a service safely."""
        switch = {"start": self.RUNNING, "stop": self.STOPPED}
        service = self.get(Constants.SERVICE_NAME_APACHE)

        if not service:
            print(Fore.RED + f"❌ Service {Constants.SERVICE_NAME_APACHE} not found.")
            return

        try:
            current_status = service["status"]
            if current_status == switch[mode]:
                print(
                    f"{Fore.YELLOW}⚠ Service {Constants.SERVICE_NAME_APACHE} "
                    f"is already {switch[mode]}."
                )
                return

            cmd = f'net {mode} "{Constants.SERVICE_NAME_APACHE}"'
            if not self.__run_command(cmd):
                print(
                    f"{Fore.RED}Error: {Fore.LIGHTYELLOW_EX}{Constants.SERVICE_NAME_APACHE}"
                    f"{Fore.RED} service could not be {mode}ed."
                )
        except Exception as e:
            print(
                f"{Fore.RED}❌ Error while trying to {mode} service "
                f"{Constants.SERVICE_NAME_APACHE}: {e}"
            )
