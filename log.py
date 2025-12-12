import datetime
import time
from threading import Thread
from itertools import cycle
from colorama import Fore, Style
import os
import getpass
from typing import Optional
from pystyle import Write, System, Colors
from enum import Enum
import re

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    SUCCESS = 4
    FAILURE = 5
    CRITICAL = 6
    ERROR = 7
    RESPONSE = 8

class Logger:
    def __init__(self, prefix: Optional[str] = "catrine.xyz/discord", level: LogLevel = LogLevel.DEBUG, log_file: Optional[str] = None):
        self.WHITE = "\u001b[37m"
        self.LIGHT_CORAL = "\033[38;5;210m"
        self.RED = "\033[38;5;196m"
        self.GREEN = "\033[38;5;40m"
        self.YELLOW = "\033[38;5;220m"
        self.CYAN = "\033[96m"


        self.DARK_BLUE = "\033[38;2;0;0;139m"  # Dark Blue
        self.BLUE = "\033[38;2;0;0;255m"  # Standard Blue
        self.LIGHT_BLUE = "\033[38;2;173;216;230m"  # Light Blue
        self.MEDIUM_BLUE = "\033[38;2;0;0;205m"  # Medium Blue
        self.ROYAL_BLUE = "\033[38;2;65;105;225m"  # Royal Blue
        self.DODGER_BLUE = "\033[38;2;30;144;255m"  # Dodger Blue
        self.RESET = "\033[0m"

        self.prefix = f"{self.DARK_BLUE}[{self.DODGER_BLUE}{prefix}{self.DARK_BLUE}] " if prefix else f"{self.DODGER_BLUE}"
        self.level = level
        self.log_file = log_file
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            self._write_to_log(f"=== Logging started at {datetime.datetime.now()} ===\n")

    def _write_to_log(self, message: str) -> None:
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    clean_message = self._strip_ansi(message)
                    f.write(clean_message + '\n')
            except Exception as e:
                print(f"Error writing to log file: {e}")

    def _strip_ansi(self, text: str) -> str:
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def get_time(self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    def message3(self, level: str, message: str, start: int = None, end: int = None) -> str:
        time = self.get_time()
        return f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DARK_BLUE}] {self.DARK_BLUE}[{self.CYAN}{level}{self.DARK_BLUE}] -> {self.CYAN}{message}{Fore.RESET}"

    def _should_log(self, message_level: LogLevel) -> bool:
        return message_level.value >= self.level.value
    
    ARROW_MARK = "⤷"
    GRAY = "\033[38;2;55;72;89m"  # #374859
    DIM = "\033[90m"

    def log_response(self, label: str, response: str, level: LogLevel = LogLevel.RESPONSE) -> None:
        if not self._should_log(level):
            return

        time = self.get_time()
        message = (
            f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DARK_BLUE}] "
            f"{self.CYAN}{self.ARROW_MARK}{self.RESET} "
            f"{self.GRAY}{label} Response:{self.RESET} "
            f"{self.DIM}{response}{self.RESET}"
        )

        print(message)

    def success(self, message: str, start: int = None, end: int = None, level: str = "Success") -> None:
        if self._should_log(LogLevel.SUCCESS):
            log_message = self.message3(f"{self.GREEN}{level}", f"{self.GREEN}{message}", start, end)
            print(log_message)
            self._write_to_log(log_message)

    def failure(self, message: str, start: int = None, end: int = None, level: str = "Failure") -> None:
        if self._should_log(LogLevel.FAILURE):
            log_message = self.message3(f"{self.RED}{level}", f"{self.RED}{message}", start, end)
            print(log_message)
            self._write_to_log(log_message)

    def error(self, message: str, start: int = None, end: int = None, level: str = "Error") -> None:
        if self._should_log(LogLevel.ERROR):
            log_message = self.message3(f"{self.RED}{level}", f"{self.RED}{message}", start, end)
            print(log_message)
            self._write_to_log(log_message)
    
    def warning(self, message: str, start: int = None, end: int = None, level: str = "Warning") -> None:
        if self._should_log(LogLevel.WARNING):
            log_message = self.message3(f"{self.YELLOW}{level}", f"{self.YELLOW}{message}", start, end)
            print(log_message)
            self._write_to_log(log_message)

    def message(self, level: str, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        timer = f" {self.DODGER_BLUE}In{self.WHITE} -> {self.DODGER_BLUE}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
        log_message = f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DODGER_BLUE}] [{self.CYAN}{level}{self.DODGER_BLUE}] -> [{self.CYAN}{message}{self.DODGER_BLUE}]{timer}"
        print(log_message)
        self._write_to_log(log_message)
    
    def message2(self, level: str, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        if start is not None and end is not None:
            print(f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DODGER_BLUE}] {self.DODGER_BLUE}[{self.CYAN}{level}{self.DODGER_BLUE}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET} [{Fore.CYAN}{end - start}s{Style.RESET_ALL}]", end="\r")
        else:
            print(f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DODGER_BLUE}] {self.DODGER_BLUE}[{Fore.BLUE}{level}{self.DODGER_BLUE}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}", end="\r")

    def question(self, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        question_message = f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DODGER_BLUE}]{Fore.RESET} {self.DODGER_BLUE}[{Fore.BLUE}?{self.DODGER_BLUE}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}"
        print(question_message, end='')
        i = input()

        if self.log_file:
            self._write_to_log(f"{question_message}")
            self._write_to_log(f"User Answer: {i}")
        
        return i

    def critical(self, message: str, start: int = None, end: int = None, level: str = "CRITICAL", exit_code: int = 1) -> None:
        if self._should_log(LogLevel.CRITICAL):
            time = self.get_time()
            log_message = f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DODGER_BLUE}]{Fore.RESET} {self.DODGER_BLUE}[{self.LIGHT_CORAL}{level}{self.DODGER_BLUE}] -> {self.LIGHT_CORAL}{message}{Fore.RESET}"
            print(log_message)
            self._write_to_log(log_message)
            input()
            self._write_to_log(f"=== Program terminated with exit code {exit_code} at {datetime.datetime.now()} ===")
            exit(exit_code)

    def info(self, message: str, start: int = None, end: int = None) -> None:
        if self._should_log(LogLevel.INFO):
            time = self.get_time()
            log_message = f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DODGER_BLUE}]{Fore.RESET} {self.DODGER_BLUE}[{Fore.BLUE}!{self.DODGER_BLUE}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}"
            print(log_message)
            self._write_to_log(log_message)

    def input(self, message: str, start: int = None, end: int = None) -> None:
        if self._should_log(LogLevel.INFO):
            time = self.get_time()
            log_message = f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DODGER_BLUE}]{Fore.RESET} {self.DODGER_BLUE}[{Fore.BLUE}?{self.DODGER_BLUE}] -> {Fore.RESET} {self.MEDIUM_BLUE}{message} {Fore.RESET}"
            returnInput = input(log_message)
            return returnInput
    
    def debug(self, message: str, start: int = None, end: int = None) -> None:
        if self._should_log(LogLevel.DEBUG):
            time = self.get_time()
            log_message = f"{self.prefix}[{self.DODGER_BLUE}{time}{self.DODGER_BLUE}]{Fore.RESET} {self.DODGER_BLUE}[{Fore.YELLOW}DEBUG{self.DODGER_BLUE}] -> {Fore.RESET} {self.GREEN}{message}{Fore.RESET}"
            print(log_message)
            self._write_to_log(log_message)

    def _parse_cooldown(self, text: str) -> int:
        if isinstance(text, (int, float)):
            return int(text) + 1

        text = text.lower().replace("minutes", "min").replace("minute", "min")\
                  .replace("seconds", "sec").replace("second", "sec")\
                  .replace("hours", "h").replace("hour", "h")\
                  .replace("days", "d").replace("day", "d")

        total = 0
        patterns = re.findall(r"(\d+)\s*(h|m|min|s|sec|d)", text)
        for num, unit in patterns:
            num = int(num)
            if unit in ["h"]:
                total += num * 3600
            elif unit in ["d"]:
                total += num * 86400
            elif unit in ["m", "min"]:
                total += num * 60
            elif unit in ["s", "sec"]:
                total += num

        if total == 0:
            if match := re.match(r"^(\d+)$", text.strip()):
                total = int(match.group(1))

        return total + 1

    def cooldown(self, duration: str | int, message: str = "Waiting for cooldown", bar_length: int = 20) -> None:
        total_seconds = self._parse_cooldown(duration)
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            remaining = total_seconds - elapsed

            if remaining <= 0:
                print(f"\r" + " " * 100 + "\r", end="")
                self.success(f"{message} finished! Ready to continue.")
                break

            mins, secs = divmod(int(remaining), 60)
            hours, mins = divmod(mins, 60)
            time_str = f"{hours:02d}:{mins:02d}:{secs:02d}" if hours else f"{mins:02d}:{secs:02d}"

            filled = int(bar_length * (elapsed / total_seconds))
            bar = f"{self.DODGER_BLUE}[{self.CYAN}{'█' * filled}{' ' * (bar_length - filled)}{self.DODGER_BLUE}]{self.RESET}"

            percent = int(100 * elapsed / total_seconds)

            cooldown_msg = (
                f"{self.prefix}[{self.DODGER_BLUE}{self.get_time()}{self.DARK_BLUE}] "
                f"{self.DARK_BLUE}[{self.LIGHT_BLUE}COOLDOWN{self.DARK_BLUE}] -> "
                f"{self.CYAN}{message} {bar} {self.YELLOW}{percent}% {self.WHITE}({time_str} left)"
            )

            print(cooldown_msg, end="\r")
            time.sleep(0.1)

log = Logger()

class Loader:
    def __init__(self, prefix: str = "catrine.xyz/discord", desc="Loading...", end="\r", timeout=0.1):
        self.desc = desc
        self.end = end
        self.prefix = prefix
        self.timeout = timeout
        self.time = datetime.datetime.now().strftime("%H:%M:%S")
        self.start_time = datetime.datetime.now()

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            loader_message = f"\r{log.PINK}[{log.MAGENTA}{self.prefix}{log.PINK}] [{log.BLUE}{log.PINK}] [{log.GREEN}{self.desc}{log.PINK}]{Fore.RESET} {c}"
            print(loader_message, flush=True, end="")
            time.sleep(self.timeout)

    def stop(self):
        self.done = True
        if self.end != "\r":
            end_message = f"\n{log.PINK}[{log.MAGENTA}{self.prefix}{log.PINK}] [{log.BLUE}{log.PINK}] {log.GREEN} {self.end} {Fore.RESET}"
            print(end_message, flush=True)
        else:
            print(self.end, flush=True)

class Home:
    def __init__(self, text, align="left", adinfo1=None, adinfo2=None, credits=None, clear=True):
        self.text = text
        self.align = align
        self.adinfo1 = adinfo1
        self.adinfo2 = adinfo2
        self.credits = credits
        self.clear = clear
        self.username = getpass.getuser()

    def _align_text(self, lines, terminal_width, alignment, block_width):
        aligned_result = []
        for line in lines:
            stripped_line = line.rstrip()
            if alignment == "center":
                padding = max(0, (terminal_width - block_width) // 2)
                aligned_line = " " * padding + stripped_line
            elif alignment == "right":
                padding = max(0, terminal_width - block_width)
                aligned_line = " " * padding + stripped_line
            else:
                aligned_line = stripped_line
            aligned_result.append(aligned_line)
        return aligned_result

    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display(self):
        char_arts, max_height = self._get_char_art()
        result = [""] * max_height

        for i in range(max_height):
            line = "".join([char_art[i] if i < len(char_art) else " " * 8 for char_art in char_arts])
            result[i] = line

        max_line_width = max(len(line) for line in result)

        try:
            terminal_width = os.get_terminal_size().columns
        except OSError:
            terminal_width = 80
        
        aligned_result = self._align_text(result, terminal_width, self.align, max_line_width)
        if self.clear:
            self._clear()

        for line in aligned_result:
            Write.Print(line + "\n", Colors.red_to_blue, interval=0.000)

        self._display_adinfo(aligned_result, terminal_width)
        self._display_welcome(terminal_width, max_line_width)


    def _display_welcome(self, terminal_width, block_width):
        welcome_message = f"Welcome {self.username}"
        if self.credits:
            welcome_message += f" | {self.credits}"

        welcome_message_with_tildes = f"    {welcome_message}    "
        tilde_line = "~" * len(welcome_message_with_tildes)

        welcome_padding = max(0, (terminal_width - len(welcome_message_with_tildes)) // 2)
        tilde_padding = max(0, (terminal_width - len(tilde_line)) // 2)

        welcome_line = " " * welcome_padding + welcome_message_with_tildes
        tilde_line_aligned = " " * tilde_padding + tilde_line

        Write.Print(f"{welcome_line}\n", Colors.red_to_blue, interval=0.000)
        Write.Print(f"{tilde_line_aligned}\n", Colors.red_to_blue, interval=0.000)

        equals_line = "═" * terminal_width
        Write.Print(f"{equals_line}\n", Colors.red_to_blue, interval=0.000)
