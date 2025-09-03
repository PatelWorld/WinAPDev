import os

from src.core.path_manager import PathManager


class Prerequisite:
    def __init__(self):
        self.root = PathManager().project_structure('prerequisite')

        # Metadata: name, file, url
        self.lists = {
            "vc2010": {
                "name": "Visual C++ 2010 Redistributable",
                "file": "vcredist_x64_2010.exe",
                "url": "https://download.microsoft.com/download/1/1/1/vcredist_x64_2010.exe",
            },
            "vc2012": {
                "name": "Visual C++ 2012 Redistributable",
                "file": "vcredist_x64_2012_(11.0.60610).exe",
                "url": "https://download.microsoft.com/download/2/2/2/vcredist_x64_2012.exe",
            },
            "vc2019": {
                "name": "Visual C++ 2019/2022 Redistributable (VS16/17)",
                "file": "VC_redist.x64_(VS16).exe",
                "url": "https://aka.ms/vs/17/release/vc_redist.x64.exe",
            },
        }

    def get_target_path(self, key: str):
        if key not in self.lists:
            raise ValueError(f"Unknown prerequisite: {key}")
        return os.path.join(self.root, self.lists[key]["file"])

    def install(self):
        pass
