#!/bin/python3

from dataclasses import dataclass, field
import shlex
import subprocess as sub
from glob import glob
import os
import sys
import uuid
import pathlib

### SETTINGS ###
REMOTE_HOST="192.168.1.64"
REMOTE_USER="omnifox"
HARDWARE_ADDRESS="6c:4b:90:21:2f:7d"

class Colortext:
    """
    Returns a colored text object.
    """
    def __init__(self, text: str) -> None:
        self.text = text
        self.ending = '\033[0m'

    def __str__(self) -> str:
        return self.text

    def __add__(self, text: str) -> 'Colortext':
        return Colortext(self.text + text)

    def bold(self) -> 'Colortext':
        self.text = '\033[1m' + self.text + self.ending
        return self

    def green(self) -> 'Colortext':
        self.text = '\033[92m' + self.text + self.ending
        return self

    def orange(self) -> 'Colortext':
        self.text = '\033[38;5;166m' + self.text + self.ending
        return self

    def red(self) -> 'Colortext':
        self.text = '\033[91m' + self.text + self.ending
        return self

    def blue(self) -> 'Colortext':
        self.text = '\033[94m' + self.text + self.ending
        return self

def wake():
    print(Colortext(f"Waking up server with hardware address: '{HARDWARE_ADDRESS}'").blue())
    sub.run(["wakeonlan", HARDWARE_ADDRESS])

def ssh():
    print(Colortext(f"Connecting to {REMOTE_USER}@{REMOTE_HOST}").blue())
    sub.run(["ssh", f"{REMOTE_USER}@{REMOTE_HOST}"])
    print(Colortext("Disconnected from remote server.").orange())

def keygen():
    try: 
        os.makedirs(f"{pathlib.Path.home()}/.ssh", exist_ok=True)
    except PermissionError:
        print(Colortext("Create REMOTE_USER user or set REMOTE_USER to the same current local user.").red())
    new_key = f"{pathlib.Path.home()}/.ssh/remote_server_{uuid.uuid4()}"
    sub.run(["ssh-keygen", "-f", new_key])
    sub.run(["ssh-copy-id", "-i", new_key, f"{REMOTE_USER}@{REMOTE_HOST}"])
    print(Colortext(f"Key '{new_key}' generated and authorized for {REMOTE_HOST}.").green())

def clean_keys(): # TODO Clean key on remote server
    keys = glob(os.path.join(pathlib.Path.home(), ".ssh", "remote_server_.*"))
    for key in keys:
        os.remove(key)
    print(Colortext(f"{len(keys)} key(s) removed.").green())
    
def shutdown_remote():
    print(Colortext(f"Shuting down remote server '{REMOTE_HOST}'").blue())
    sub.run(["ssh", f"{REMOTE_USER}@{REMOTE_HOST}", "sudo shutdown -P 0"])

def reboot_remote():
    print(Colortext(f"Rebooting remote server '{REMOTE_HOST}'"))
    sub.run(["ssh", f"{REMOTE_USER}@{REMOTE_HOST}", "sudo shutdown -r 0"])

def console_clear() -> None:
    os.system('clear')

def help():
    print(f"""{Colortext("Commands:").bold()}
  {Colortext("help | h").bold()} : This.
  {Colortext("wake | w").bold()} : Wake on lan remote server
  {Colortext("ssh").bold()} : ssh connexion to remote server
  {Colortext("keygen").bold()} : Generate a new ssh key for the current user and install it {Colortext("(BROKEN)").red()}
  {Colortext("clean_keys").bold()} : Remove every generated ssh key {Colortext("(BROKEN)").red()}
  {Colortext("shutdown | s | off").bold()} : Shutdown remote server {Colortext("(BROKEN)").red()}
  {Colortext("reboot | r").bold()} : Reboot remote server {Colortext("(BROKEN)").red()}
  {Colortext("quit | q | exit").bold()} : Quit this CLI
""")

@dataclass(frozen=True, slots=True)
class InputCommand:
    """Class that represents a command_name."""
    command_name: str
    arguments: list[str] = field(default_factory=list)

def run_command(command: InputCommand) -> None:
    match command:
        case InputCommand(command_name="help" | "h"):
            help()

        case InputCommand(command_name="wake" | "w"):
            wake()

        case InputCommand(command_name="ssh"):
            ssh()

        case InputCommand(command_name="keygen"):
            keygen()

        case InputCommand(command_name="clean_keys"):
            clean_keys()

        case InputCommand(command_name="s" | "shutdown" | "off"):
            shutdown_remote()

        case InputCommand(command_name="reboot" | "r"):
            shutdown_remote()

        case InputCommand(command_name="quit" | "q" | "exit", arguments=[*_]):
            console_clear()
            sys.exit(0)

        case _:
            print(Colortext(f"Unknown command {command.command_name}.").red())

def display_title():
    print(Colortext("""\
                                                          .--.
                                                   _      |__| .-------.
      _,-=._          /|_/|        __ ___ __ _____| |     |=.| |.-----.|
  `-.}   `=._,.-=-._.,  @ @._,    / _` \ V  V / _ \ |     |--| ||$qwol||
     `._ _,-.   )      _,.-'      \__, |\_/\_/\___/_|     |  | |'-----'|
        `    G.m-"^m`m'              |_|                  |__|~')_____('
""").orange())
    print(Colortext('Quick WoL CLI').bold().green())
    print(Colortext('Version: ').bold() + '0.1.0')
    print(Colortext('Author: ').bold() + 'Yoann Renard')
    print(Colortext('License: ').bold() + 'MIT')
    print(Colortext('Github: ').bold() + 'https://github.com/Yoann-Renard/misc' + '\n')

if __name__ == "__main__":
    console_clear()
    display_title()
    try:
        while True:
            try:
                command, *arguments = shlex.split(input(">> "))
                run_command(InputCommand(command, arguments))
            except ValueError:
                pass
    except (KeyboardInterrupt, EOFError):
        console_clear()
        sys.exit(0)
        

