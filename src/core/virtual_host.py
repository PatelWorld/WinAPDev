import os

from src.core.certificate_manager import CertificateManager
from src.core.cli_arguments import Arguments
from src.core.path_manager import PathManager
from src.core.system_paths import SystemPaths
from src.core.windows_host_manager import WindowsHostsManager


class VirtualHost:
    HOSTS_FILE = (
        SystemPaths().system_host
    )  # Typically C:\Windows\System32\drivers\etc\hosts

    def __init__(self):
        self.path_manager = PathManager()
        self.apache_v_host = self.path_manager.deploy_structure('httpd_vhost_conf')
        if not os.path.exists(self.apache_v_host):
            raise FileNotFoundError(f"Apache config not found: {self.apache_v_host}")

    def add(self, hostname, port, app_root, ssl=False, balancer=False, members=None):
        # 1. SSL Certs
        if ssl:
            CertificateManager.create(self.apache_v_host, hostname)

        # 2. Config
        if balancer:
            config = self.build_balancer(hostname, port, members or [])
        else:
            config = self.build(hostname, port, app_root, ssl)

        # 3. Append config to Apache
        with open(self.apache_v_host, "a") as f:
            f.write(config + "\n")

        # 4. Update hosts file
        WindowsHostsManager().add_entry(hostname)

    def remove(self, hostname):
        # Remove from apache conf
        with open(self.apache_v_host, "r") as f:
            lines = f.readlines()
        with open(self.apache_v_host, "w") as f:
            f.writelines([line for line in lines if hostname not in line])

        # Remove from hosts
        WindowsHostsManager().delete_entry(hostname)

    def add_project(self, args: Arguments):
        hostname = args.get("hostname")
        if hostname is None:
            raise RuntimeError("Wrong hostname provided")

        root_dir = args.get("dir")
        if root_dir is None:
            raise RuntimeError("Wrong")

        port = args.get("port", 80)

        self.add(hostname, port, root_dir)

    def remove_project(self, args: Arguments):
        hostname = args.get("hostname")
        if hostname is None:
            raise RuntimeError("Wrong hostname provided")

        self.remove(hostname)

    @staticmethod
    def build(hostname, port, app_root, ssl=False):
        ssl_block = (
            f"""
                \nSSLEngine on
                SSLCertificateKeyFile "cert/{hostname}.key"
                SSLCertificateFile "cert/{hostname}.crt"
            """
            if ssl
            else ""
        )

        return f"""
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

    @staticmethod
    def build_balancer(hostname, port, members, ssl=False):
        balancer_members = "\n".join([f"BalancerMember {m}" for m in members])
        return f"""
            <VirtualHost *:{port}>
                ProxyRequests Off
                ProxyPass / balancer://mycluster/
                <Proxy balancer://mycluster>
                    {balancer_members}
                </Proxy>
            </VirtualHost>
            """
