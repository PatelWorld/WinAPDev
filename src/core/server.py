import os
from pathlib import Path

from colorama import init, Fore

from src.core.app_structure import AppStructure
from src.core.batch_file_creator import BatchFileCreator
from src.core.binaries import Binaries
from src.core.console_logger import ConsoleLogger
from src.core.constants import Constants
from src.core.env_path_manager import EnvPathManager
from src.core.extractor import Extractor
from src.core.file_downloader import FileDownloader
from src.core.path_manager import PathManager
from src.core.prerequisite import Prerequisite
from src.core.service import Service
from src.core.templates import Templates
from src.core.virtual_host import VirtualHost

init(autoreset=True)


class Server:
    def __init__(self):
        self.path_manager = PathManager()

    def init(self):
        if os.path.exists(self.path_manager.deploy_root()):
            print(f"{Fore.RED}Error: Server already setup and running")
            exit()
        Prerequisite().install()
        AppStructure(self.path_manager.deploy_root()).create()
        self.__extract_binaries()

    def setup(self):
        self.init()
        self.__configure()
        self.__write_env()
        self.__write_batch()
        Service().install()
        Service().start()
        self.__open_app()

    def conf(self):
        Service().stop()
        self.__configure()
        Service().install()
        Service().start()

    def update(self):
        Service().stop()
        self.__configure()
        Service().start()

    def clear(self):
        if os.path.exists(self.path_manager.deploy_root()):
            Service().remove()
            AppStructure(self.path_manager.deploy_root()).delete()
            self.__clear_env()
        else:
            print(
                f"{Fore.RED}Error: {Fore.CYAN}{self.path_manager.deploy_structure(Constants.KEY_ROOT)}{Fore.RED} not found, Either it's not installed yet or already deleted."
            )

    @classmethod
    def __extract_binaries(cls):
        print(f"{Fore.GREEN}Extracting binaries...")
        binary_root = Path(__file__).resolve().parents[1] / "binary"
        binaries = Binaries()
        for k, v in binaries.get().items():
            source_file = binary_root / v.get("file")
            target_path = os.path.join(PathManager().deploy_structure(Constants.DIR_BIN), k, Path(source_file).stem)
            if not os.path.exists(source_file):
                print(f"Source file not found, attempting to download...")
                FileDownloader(binary_root).download(v.get("url"))
            else:
                print(f"Source file found in binary")

            Extractor().extract(source_file, target_path)

    def __configure(self):
        self.__create_server_index_file()
        Templates().deploy()
        VirtualHost().add("dev.local", 80, self.path_manager.deploy_structure(Constants.DIR_WWW))

    def __write_env(self):
        EnvPathManager(system=True).add(self.path_manager.deploy_structure(Constants.DIR_COMMAND))
        ConsoleLogger.info("Command path added to system environment variable")

    def __clear_env(self):
        EnvPathManager(system=True).delete(self.path_manager.deploy_structure(Constants.DIR_COMMAND))
        ConsoleLogger.info("Command path deleted from system environment variable")

    def __create_server_index_file(self):
        print(f"{Fore.GREEN}Creating server index file...")

        with open(self.path_manager.deploy_structure("index"), "w") as f:
            f.write("""
                <html>
                    <body style="padding:20px;font-family: Verdana, Geneva, Tahoma, sans-serif;">
                        <h1 style="text-align:center;color:green">Welcome to AMP Server</h1>
                        <p>Powered By - PatelWorld</p>
                    </body>
                </html>
            """)

    def __open_app(self):
        cmd = f"start chrome http://dev.local:80"
        print(
            f"\nApplication URL: http://dev.local:80"
        )
        os.system(cmd)

    def __write_batch(self):
        command_file = os.path.join(self.path_manager.deploy_structure(Constants.DIR_COMMAND),"php.env.bat")
        BatchFileCreator(self.path_manager.project_structure(Constants.KEY_ROOT), command_file).create_batch()
        # target_file = os.path.join(self.path_manager.paths.system32, "php.env.bat")
        # os.system(f"mklink /D {target_file} {command_file}")