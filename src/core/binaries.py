from os.path import dirname


class Binaries:
    def __init__(self):
        # self.path_manager = PathManager()
        # self.root = os.path.join(self.path_manager.project(Constants.KEY_ROOT), "src", "binary")
        # self.deployment_structure = self.path_manager.__structure.get(Constants.DIR_BIN)

        self.__items = {
            "apache": {
                "name": "Apache HTTPD",
                "version": "2.4.65",
                "file": "httpd-2.4.65-250724-Win64-VS17.zip",
                "checksum": "E324797985825424AF00CDB9D78B029723F18862DF6C02C2219B341E33E31F04",  # Placeholder checksum
                "url": "https://www.apachelounge.com/download/VS17/binaries/httpd-2.4.65-250724-Win64-VS17.zip",
                "source": dirname(__file__)
                # "target": os.path.join(self.path_manager.get_structure(Constants.DIR_BIN), Constants.DIR_APACHE)
            },
            "php": {
                "name": "PHP",
                "version": "8.1.0",
                "file": "php-8.4.12-Win32-vs17-x64.zip",
                "checksum": "602dbfd1a65e99e8bb29c7ff2c8a7888f3cd72a8162de99b7860bbe117779d1c456",
                # Placeholder checksum
                "url": "https://windows.php.net/downloads/releases/php-8.4.12-Win32-vs17-x64.zip",
                "source": dirname(__file__),
                # "target": os.path.join(self.path_manager.get_structure(Constants.DIR_BIN), Constants.DIR_PHP)
            },
        }

    def get(self):
        return self.__items
