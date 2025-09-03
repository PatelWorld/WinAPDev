import os
import subprocess


class CertificateManager:
    @staticmethod
    def create(apache_root, hostname, force=False):
        cert_dir = os.path.join(apache_root, "cert")
        os.makedirs(cert_dir, exist_ok=True)

        crt_file = os.path.join(cert_dir, f"{hostname}.crt")
        key_file = os.path.join(cert_dir, f"{hostname}.key")

        if not force and os.path.exists(crt_file):
            return crt_file, key_file

        cmd = [
            "openssl",
            "req",
            "-x509",
            "-nodes",
            "-days",
            "3650",
            "-newkey",
            "rsa:2048",
            "-keyout",
            key_file,
            "-out",
            crt_file,
            "-subj",
            f"/CN={hostname}/O=Dev/C=IN",
        ]
        subprocess.run(cmd, check=True)
        return crt_file, key_file
