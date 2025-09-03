from colorama import Fore, Back, Style, init

# Auto reset after each print
init(autoreset=True)


class ConsoleLogger:
    @staticmethod
    def success(message: str):
        print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + message)

    @staticmethod
    def error(message: str):
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + message)

    @staticmethod
    def warning(message: str):
        print(Fore.YELLOW + "[WARNING] " + Style.RESET_ALL + message)

    @staticmethod
    def info(message: str):
        print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + message)

    @staticmethod
    def debug(message: str):
        print(Fore.MAGENTA + "[DEBUG] " + Style.RESET_ALL + message)

    @staticmethod
    def critical(message: str):
        print(Back.RED + Fore.WHITE + "[CRITICAL] " + Style.RESET_ALL + message)

    @staticmethod
    def custom(message: str, fore_color=Fore.WHITE, back_color="", style=Style.NORMAL):
        """Allow custom color logging"""
        print(f"{back_color}{fore_color}{style}{message}{Style.RESET_ALL}")
