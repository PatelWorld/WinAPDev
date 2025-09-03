import os
import shutil

# from src.core.path_manager import PathManager
from colorama import Fore, init

from src.core.constants import Constants

init(autoreset=True)


class AppStructure:
    def __init__(self, root):
        self.root_path = root
        self.folders = [Constants.DIR_BIN, Constants.DIR_WWW, Constants.DIR_COMMAND, Constants.DIR_TEMP,
                        Constants.DIR_LOGS]

    def create(self):
        try:
            os.makedirs(self.root_path, exist_ok=True)
            for folder in self.folders:
                target_dir = os.path.join(self.root_path, folder)
                os.makedirs(target_dir, exist_ok=True)
                print(Fore.GREEN + f"[CREATED] {target_dir}")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to create folders: {e}")

    def delete(self):
        try:
            if os.path.exists(self.root_path):
                shutil.rmtree(self.root_path)
                print(Fore.YELLOW + f"[DELETED] {self.root_path}")
            else:
                print(Fore.CYAN + f"[INFO] Nothing to delete, {self.root_path} does not exist")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to delete structure: {e}")
