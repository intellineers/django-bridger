import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter


class PrintColor:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_bold(text, color=None):
    if color:
        print(f"{PrintColor.BOLD}{color}{text}{PrintColor.END}")
    else:
        print(f"{PrintColor.BOLD}{text}{PrintColor.END}")


def print_dict(dictionary):
    print(highlight(json.dumps(dictionary, indent=4), JsonLexer(), TerminalFormatter()))
