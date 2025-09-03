# -------------------------------------------
# Python version used 3.13.3 64 bit
# Pip - v0.8.13
# -------------------------------------------

import sys
import traceback
from src.core.service import Service
from src.core.server import Server
from colorama import init, Fore, Back
from collections import defaultdict

init(autoreset=True)


def show_help():
    print(Fore.YELLOW + "\nAvailable Commands:\n" + "-" * 80)

    # Group commands automatically by prefix (server, app, service, config, etc.)
    grouped = defaultdict(list)
    for cmd, meta in registered_commands.items():
        if ":" in cmd:
            prefix = cmd.split(":")[0].capitalize()
        else:
            prefix = "Misc"
        grouped[prefix].append((cmd, meta["desc"]))

    # Print category wise
    for category, cmds in grouped.items():
        print(Fore.GREEN + f"\n[{category} Commands]")
        for cmd, desc in cmds:
            print(Fore.CYAN + f"  {cmd:<18}" + Fore.WHITE + f" {desc}")

    print(Fore.YELLOW + "-" * 80)


try:
    registered_commands = {
        "dev:setup": {
            "func": lambda: Server().setup(),
            "desc": "Setup fresh server stack for PHP development environment"
        },
        "dev:clear": {
            "func": lambda: Server().clear(),
            "desc": "Clear,Delete development environment"
        },
        # "server:init": {
        #     "func": lambda: Server().init(),
        #     "desc": "Initialize the server stack"
        # },
        "server:conf": {
            "func": lambda: Server().conf(),
            "desc": "Configure server settings"
        },
        "server:update": {
            "func": lambda: Server().update(),
            "desc": "Update the server stack"
        },
        # "app:init": {
        #     "func": lambda: App().init(),
        #     "desc": "Initialize the application"
        # },
        # "app:conf": {
        #     "func": lambda: App().conf(),
        #     "desc": "Configure application settings"
        # },
        # "app:update": {
        #     "func": lambda: App().update(),
        #     "desc": "Update application stack"
        # },
        # "app:migrate": {
        #     "func": lambda: App().migrate(),
        #     "desc": "Run database migrations"
        # },
        # "app:open": {
        #     "func": lambda: App().open(),
        #     "desc": "Open the application in browser"
        # },
        "service:install": {
            "func": lambda: Service().install(),
            "desc": "Install background service"
        },
        "service:remove": {
            "func": lambda: Service().remove(),
            "desc": "Remove background service"
        },
        "service:start": {
            "func": lambda: Service().start(),
            "desc": "Start service"
        },
        "service:stop": {
            "func": lambda: Service().stop(),
            "desc": "Stop service"
        },
        "service:restart": {
            "func": lambda: Service().restart(),
            "desc": "Restart service"
        },
        "config:show": {
            "func": lambda: print("Not implemented yet"),
            "desc": "Show current configuration"
        },
        "help": {
            "func": lambda: show_help(),
            "desc": "Show this help message"
        },
    }

    # No command provided → show help
    if len(sys.argv) < 2:
        print(Back.RED + " Error: No command provided.")
        show_help()
        sys.exit(1)

    command = sys.argv[1]

    if command in registered_commands:
        registered_commands[command]['func']()
    else:
        print(f"{Back.RED} Error: Unknown command '{command}'")
        show_help()

except Exception:
    traceback.print_exc()
