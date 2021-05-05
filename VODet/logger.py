import sys
from colorama import init, Fore, Back, Style
init(convert = True)
init(autoreset=True)
class Logger:
    @staticmethod
    def print_fail(message, end = '\n'):
        print(Fore.RED + message, end=end)

    @staticmethod
    def print_pass(message, end = '\n'):
        print(Fore.GREEN + message, end=end)

    @staticmethod
    def print_warn(message, end = '\n'):
        print(Fore.YELLOW + message, end=end)

    @staticmethod
    def print_info(message, end = '\n'):
        print(Fore.BLUE + message, end=end)

    @staticmethod
    def print_bold(message, end = '\n'):
        print(Style.BRIGHT + message, end=end)

    @staticmethod
    def exit_line():
        sys.stdout.write("\n")