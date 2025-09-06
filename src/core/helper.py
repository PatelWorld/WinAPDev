import os.path
import webbrowser


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def change_to_forward_slash(s):
        return s.replace("\\", "/")

    @staticmethod
    def replace_tokens(destination, tokens_list):
        with open(destination, "r+") as fp:
            file_data = fp.read()
            for eachToken, token_value in tokens_list.items():
                token = (
                    f"[#{eachToken}#]"
                    if isinstance(token_value, str)
                    else f"'[#{eachToken}#]'"
                )
                if not isinstance(token_value, str):
                    token_value = str(token_value)
                file_data = file_data.replace(token, token_value)

            fp.seek(0)
            fp.truncate()
            fp.write(file_data)
        fp.close()

    @staticmethod
    def open_app(hostname: str, port: int = 80, ssl: bool = False):
        scheme = "https" if ssl else "http"
        url = f"{scheme}://{hostname}:{port}"
        print(f"\nApplication URL: {url}")
        webbrowser.open(url)  # opens in default browser

