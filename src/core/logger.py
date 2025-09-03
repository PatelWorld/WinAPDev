import datetime
import json
import os


# from src.core.core import Root


class Logger:
    def __init__(self, log_root=None, auto_json=False):
        # self.PATH = Root()
        self.log_root = log_root  # or self.PATH.BUILDER.LOG
        self.auto_json = auto_json

    def __ensure_dir(self, level):
        """Ensure log directory exists for given level."""
        log_dir = os.path.join(self.log_root, level)
        os.makedirs(log_dir, exist_ok=True)
        return log_dir

    def __format_data(self, data):
        """Convert dicts/objects to JSON if enabled."""
        if self.auto_json:
            try:
                return json.dumps(data, ensure_ascii=False, indent=2)
            except Exception:
                return str(data)
        return str(data)

    def __log(self, level, data, file_name):
        log_dir = self.__ensure_dir(level)
        absolute_file_path = os.path.join(log_dir, file_name)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = self.__format_data(data)
        log_line = f"[{timestamp}] {formatted}\n"

        try:
            with open(absolute_file_path, "a", encoding="utf-8") as file:
                file.write(log_line)
        except Exception as e:
            # Fallback to console if file write fails
            print(f"Logging error: {e}")
            print(log_line)

    def debug(self, data, file_name="debug.log"):
        self.__log("debug", data, file_name)

    def error(self, data, file_name="error.log"):
        self.__log("error", data, file_name)

    def dev(self, data, file_name="dev.log"):
        self.__log("dev", data, file_name)

    def info(self, data, file_name="info.log"):
        self.__log("info", data, file_name)
