import os
import shutil

class BatchFileCreator:
    def __init__(self, project_path, output_name="php.env.bat"):
        self.project_path = os.path.abspath(project_path)
        self.venv_activate = os.path.join(self.project_path, ".venv", "Scripts", "activate.bat")
        self.output_name = output_name

    def create_batch(self):
        """Create batch file to launch Admin CMD with venv"""
        content = f"""@echo off
:: Auto-generated batch file to open Admin CMD with venv

set "PROJECT_PATH={self.project_path}"
set "VENV_PATH={self.venv_activate}"

echo Launching Command Prompt as Administrator...
powershell -Command "Start-Process cmd -ArgumentList '/k cd /d \"%PROJECT_PATH%\" && call \"%VENV_PATH%\"' -Verb RunAs"
"""
        with open(self.output_name, "w") as f:
            f.write(content)
        f.close()
        # # Optional: copy to System32 so it's available everywhere
        # system32 = os.path.join(os.environ["WINDIR"], "System32")
        # dest = os.path.join(system32, self.output_name)
        # try:
        #     shutil.copy2(self.output_name, dest)
        #     print(f"[SUCCESS] Batch file created globally: {dest}")
        # except PermissionError:
        #     print(f"[WARNING] Could not copy to {system32}. Run as Administrator to install globally.")
        # else:
        #     print("Now you can type `php.env` in Run (Win+R) or any CMD window.")

# Example usage
if __name__ == "__main__":
    project_dir = r"C:\Users\YourName\MyProject"   # <-- change this
    creator = BatchFileCreator(project_dir, "php.env.bat")
    creator.create_batch()
