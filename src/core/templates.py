import os
import shutil

from src.core.constants import Constants
from src.core.helper import Helper
from src.core.path_manager import PathManager


class Templates:
    def __init__(self):
        self.path_manager = PathManager()
        self.source_template = self.path_manager.project_structure('templates')
        self.deployment_structure = self.path_manager.deploy_structure(Constants.DIR_BIN)

        # Example template categories
        self.__lists = {
            "apache_conf": {
                "name": "Apache httpd config Template",
                "description": "Apache main configuration file",
                "file": "httpd.conf",
                "source": os.path.join(self.path_manager.project_structure("templates"), "httpd.conf"),
                "target": self.path_manager.deploy_structure("httpd_conf"),
                "tokens": {
                    'APACHE_ROOT': self.path_manager.deploy_structure('apache_root'),
                    'SERVER_NAME': "localhost",
                    'APP_SERVER_WWW': self.path_manager.deploy_structure(Constants.DIR_WWW),
                    'PHP_ROOT': self.path_manager.deploy_structure("php_root"),
                }
            },
            "php_ini": {
                "name": "PHP ini Template",
                "description": "Base php.ini template",
                "file": "php.ini",
                "source": os.path.join(self.path_manager.project_structure("templates"), "php.ini"),
                "target": self.path_manager.deploy_structure("php_ini"),
                "tokens": {
                    'DEPLOYMENT_ROOT': str(self.path_manager.deploy_root()),
                    'PHP_ROOT': self.path_manager.deploy_structure('php_root'),
                    'PHP_TIMEZONE': '"UTC"'
                }
            },
        }

    def deploy(self):
        """This will transfer the base template with token to target place then token will be replaced based on current setup"""
        for k, v in self.__lists.items():
            if v.get('source') and v.get('target'):
                shutil.copy2(v.get('source'), v.get('target'))
                Helper.replace_tokens(v.get('target'), v.get('tokens'))
