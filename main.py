
import os, re, time, queue, shutil, ctypes, random, threading, requests, json
from tqdm import tqdm
from getpass import getpass
from urllib.parse import urlparse, urlencode, parse_qs, quote
from typing import Dict, List, Optional, Tuple
from colorama import init, Fore, Style
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System


class zNGL:

    def __init__(self,
                 _username: str = "",
                 _threads: int = 1,
                 _question: str = ""):
        self.messages: List[str] = []
        self._username = _username
        self._threads = _threads
        self._question = _question
        self._ngl = "https://ngl.link/api/submit"
        self._timeout = 15
        self.NAME_TOOL = "zNGL Tool"
        self.VERSION_TOOL = "v1.0.0"
        if os.name == "nt":
            os.system(
                f"title 💰 {self.NAME_TOOL} {self.VERSION_TOOL} by telegram @Marine 💰"
            )
        device_id = f"{self._random_str(8)}-{self._random_str(4)}-{self._random_str(4)}-{self._random_str(4)}-{self._random_str(12)}"
        _data = {
            "distinct_id": f"$device:{device_id}",
            "device_id": device_id,
            "initial_referrer": "$direct",
            "initial_referring_domain": "$direct",
            "mps": {},
            "mpso": {
                "initial_referrer": "$direct",
                "initial_referring_domain": "$direct",
            },
            "mpus": {},
        }
        self.base_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language":
            "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":
            f"_ga=GA1.1.{random.randint(1000000000, 9999999999)}.{random.randint(1000000000, 9999999999)}; mp_{self._random_str(32)}_mixpanel={quote(json.dumps(_data))}",
            "Host": "ngl.link",
            "Origin": "https://ngl.link",
            "sec-ch-ua":
            '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.successful_runs = 0
        self.success_lock = threading.Lock()
        self.should_stop = False
        self.print_lock = threading.Lock()
        self.print_queue = queue.Queue()

        Anime.Fade(
            Center.Center(self.landing()),
            Colors.red_to_yellow,
            Colorate.Vertical,
            enter=True,
        )
        self._input()
        self.base_headers["Referer"] = f"https://ngl.link/{self._username}"

    def _convert(self, input_str: str) -> Optional[str]:
        input_str = input_str.strip()
        if input_str.startswith("https://ngl.link/"):
            try:
                _parsed = urlparse(input_str)
                if _parsed.scheme != "https" or _parsed.netloc != "ngl.link":
                    return None
                username = _parsed.path.lstrip("/")
                if not username:
                    return None
                return username
            except Exception:
                return None
        else:
            if not input_str:
                return None
            return input_str

    def _check_user(self, username: str) -> bool:
        try:
            response = requests.get(
                f"https://ngl.link/{username}",
                headers={
                    "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                    "Accept": "text/html",
                },
                timeout=self._timeout,
                verify=True,
            )
            return "Could not find user" not in response.text
        except Exception:
            return False

    def _input(self):
        while True:
            _user = Write.Input(
                "[+] Nhập Link NGL hoặc Username > ",
                Colors.red_to_yellow,
                interval=0.005,
            ).strip()
            if not _user:
                print(
                    f"{Fore.RED}⚠️ Vui lòng nhập Username hoặc Link cần spam.{Style.RESET_ALL}"
                )
                continue
            self._username = self._convert(_user)
            if not self._username:
                print(
                    f"{Fore.RED}⚠️ Vui lòng nhập username hoặc URL (eg: https://ngl.link/username){Style.RESET_ALL}"
                )
                continue
            if not self._check_user(self._username):
                print(
                    f"{Fore.RED}⚠️ Người dùng '{self._username}' không tồn tại.{Style.RESET_ALL}"
                )
                continue
            break
        while True:
            try:
                self._threads = int(
                    Write.Input(
                        "[+] Nhập Threads (1 - 500) > ",
                        Colors.red_to_yellow,
                        interval=0.005,
                    ).strip())
                if self._threads < 1 or self._threads > 500:
                    print(
                        f"{Fore.RED}⚠️ Số Threads Tối Thiểu Là 1, Tối Đa Là 500, Số Threads Càng Cao {self.NAME_TOOL} Request Càng Nhiều.{Style.RESET_ALL}"
                    )
                    continue
                break
            except ValueError:
                print(f"{Fore.RED}⚠️ Threads Phải Là Số.{Style.RESET_ALL}")
        while True:
            self._question = Write.Input(
                "[+] Nhập Thông Điệp (Có Thể Để Trống) > ",
                Colors.red_to_yellow,
                interval=0.005,
            ).strip()
            if self._question == "":
                self._question = self.NAME_TOOL
                break
            if len(self._question) > 70:
                print(
                    f"{Fore.RED}⚠️ Thông Điệp Không Được Quá Dài (Tối Đa 70 Ký Tự).{Style.RESET_ALL}"
                )
                continue
            break
        if (Write.Input(
                "[?] Kích Hoạt Random Emoji (yes/no) > ",
                Colors.red_to_yellow,
                interval=0.005,
        ).strip().lower() == "yes"):
            self.enable_emoji = True
        else:
            self.enable_emoji = False

    def landing(self):
        return f"""
     {self.NAME_TOOL} - {self.VERSION_TOOL}

███████████████████████████
███████▀▀▀░░░░░░░▀▀▀███████
████▀░░░░░░░░░░░░░░░░░▀████
███│░░░░░░░░░░░░░░░░░░░│███
██▌│░░░░░░░░░░░░░░░░░░░│▐██
██░└┐░░░░░░░░░░░░░░░░░┌┘░██
██░░└┐░░░░░░░░░░░░░░░┌┘░░██
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
██▌░│██████▌░░░▐██████│░▐██
███░│▐███▀▀░░▄░░▀▀███▌│░███
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
████▄─┘██▌░░░░░░░▐██└─▄████
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
███████▄░░░░░░░░░░░▄███████
██████████▄▄▄▄▄▄▄██████████
███████████████████████████

Press [ENTER] to continue...
"""

    def banner(self):
        os.system("cls" if os.name == "nt" else "clear")
        text = """

███████╗░░░░░░███╗░░██╗░██████╗░██╗░░░░░  ████████╗░█████╗░░█████╗░██╗░░░░░
╚════██║░░░░░░████╗░██║██╔════╝░██║░░░░░  ╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
░░███╔═╝█████╗██╔██╗██║██║░░██╗░██║░░░░░  ░░░██║░░░██║░░██║██║░░██║██║░░░░░
██╔══╝░░╚════╝██║╚████║██║░░╚██╗██║░░░░░  ░░░██║░░░██║░░██║██║░░██║██║░░░░░
███████╗░░░░░░██║░╚███║╚██████╔╝███████╗  ░░░██║░░░╚█████╔╝╚█████╔╝███████╗
╚══════╝░░░░░░╚═╝░░╚══╝░╚═════╝░╚══════╝  ░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝
"""
        lines = text.strip("\n").split("\n")
        colors = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.RED]
        _terminal = shutil.get_terminal_size().columns
        print("\n" * 1)
        print(f"{self.NAME_TOOL} {self.VERSION_TOOL}".rjust(100))
        print("")
        for color, line in zip(colors, lines):
            padding = (_terminal - len(line)) // 2
            print(color + " " * padding + line)

    def change_title(self, arg):
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(arg)

    def exit(self, sig, frame):
        os._exit(0)

    def _random_str(
            self,
            length: int = 10,
            chars: str = "abcdefghijklmnopqrstuvwxyz0123456789") -> str:
        return "".join(random.choice(chars) for _ in range(length))

    def _random_num(self, length=6) -> str:
        return "".join(random.choices("0123456789", k=length))

    def _rainbow_text(self, text: str) -> str:
        rainbow_colors = [
            Fore.RED,
            Fore.YELLOW,
            Fore.GREEN,
            Fore.CYAN,
            Fore.BLUE,
            Fore.MAGENTA,
        ]
        rainbow_str = ""
        for i, char in enumerate(text):
            rainbow_str += rainbow_colors[i % len(rainbow_colors)] + char
        return rainbow_str + Style.RESET_ALL

    def zNGL(self, thread_id: int):
        icon = (random.choice([
            " 😊", " 😎", " 😍", " 😉", " 😁", " 😄", " 😃", " 🙂", " 😆", " 😅", " 🤣",
            " 😂", " 😋", " 😛", " 😜", " 🤪", " 🤩", " 🥰", " 😇", " 🙃", " 🥹", " 😌",
            " 🤗", " 😏", " 🤭", " 🫢", " 🫠", " 🤫", " 😭", " 😢", " 😥", " 😓", " 😞",
            " 😔", " 🙁", " ☹️", " 😠", " 😡", " 🤬", " 😤", " 😖", " 😫", " 😩", " 🥺",
            " 😱", " 😨", " 😰", " 😵", " 🤯", " 😳", " 😬", " 🫣", " 🥴", " 🤢", " 🤮",
            " 😷", " 🤒", " 🤕", " 🤧", " 🥶", " 🥵", " 😈", " 👿", " 💀", " 👻", " 👽",
            " 😺", " 😸", " 😹", " 😻", " 😼", " 😽", " 🙀", " 😿", " 😾", " 🤡", " ❤️",
            " 🧡", " 💛", " 💚", " 💙", " 💜", " 🤎", " 🖤", " 🤍", " 💓", " 💗", " 💖",
            " 💘", " 💝", " 💞", " 💕"
        ]) if getattr(self, "enable_emoji", False) else "")
        try:
            data = {
                "username": self._username,
                "question": self._question + icon,
                "deviceId": self._random_str(36),
                "gameSlug": "",
                "referrer": "",
            }
            response = requests.post(
                self._ngl,
                headers=self.base_headers,
                data=urlencode(data),
                timeout=self._timeout,
                verify=True,
            )
            response.raise_for_status()
            with self.success_lock:
                self.successful_runs += 1
                # Stop when we reach the target number of messages
                if self.successful_runs >= self._threads:
                    self.should_stop = True
                    print(f"{Fore.GREEN}🎯 Đã đạt đủ số lượng tin nhắn ({self.successful_runs}/{self._threads}). Tự động dừng tấn công.{Style.RESET_ALL}")
            self.print_queue.put((
                f"{Fore.MAGENTA}ID-{self._random_num(5)} {Fore.GREEN}•{Style.RESET_ALL} "
                f"{self._rainbow_text('[' + time.strftime('%H:%M:%S %d/%m/%Y') + ']')} "
                f"{Fore.GREEN}|{Style.RESET_ALL} "
                f"{Fore.RED}NGL Username: [{Fore.YELLOW}{self._username + icon}{Style.RESET_ALL}] "
                f"{Fore.GREEN}|{Style.RESET_ALL} "
                f"{Fore.RED}Question: [{Fore.YELLOW}{self._question}{Style.RESET_ALL}] "
                                 f"({Fore.GREEN}{self.successful_runs}{Style.RESET_ALL}/"
                 f"{Fore.RED}{self._threads}{Style.RESET_ALL})"))

            return True
        except Exception as e:
            self.messages.append(f"ERROR: {str(e)}")
            return False

    def thread_worker(self, thread_id: int):
        try:
            self.zNGL(thread_id)
        except Exception as e:
            self.messages.append(f"ERROR: {str(e)}")

    def printer_worker(self):
        while not self.should_stop:
            try:
                message = self.print_queue.get(timeout=0.1)
                with self.print_lock:
                    print(message)
                self.print_queue.task_done()
            except queue.Empty:
                time.sleep(0.01)
            except Exception:
                pass

    def run(self,
            target: str = None,
            threads: int = None,
            note: str = None) -> None:
        target = target or self._username
        threads = threads or self._threads
        note = note or self._question
        self.should_stop = False
        self.successful_runs = 0
        cycle_count = 0
        printer_thread = threading.Thread(target=self.printer_worker)
        printer_thread.daemon = True
        printer_thread.start()
        print("")
        print("".join([
            f"{[Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLUE_EX, Fore.CYAN, Fore.LIGHTGREEN_EX, Fore.GREEN][i * 6 // len('»»————————————————————————————————————————««')]}{c}"
            for i, c in enumerate(
                "»»————————————————————————————————————————««")
        ]) + Style.RESET_ALL)
        print(f"""\033[1;32m[+] NGL Username: {target or 'None'} 
\033[35m[+] Question: {note or 'None'}
\033[34m[+] Threads: {threads or 'None'}
\033[0;31m[+] Telegram: @Marine""")
        print("".join([
            c for i, c in enumerate(
                "»»————————————————————————————————————————««")
            for c in [
                f"{[Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLUE_EX, Fore.CYAN, Fore.LIGHTGREEN_EX, Fore.GREEN][i * 6 // len('»»————————————————————————————————————————««')]}{c}"
            ]
        ]) + Style.RESET_ALL)
        print(
            f"{Fore.GREEN}Starting attack with {threads} concurrent threads...{Style.RESET_ALL}"
        )
        try:
            while True:
                if self.should_stop or self.successful_runs >= threads:
                    break
                cycle_count += 1
                thread_list = []
                start_time = time.time()
                for i in range(threads):
                    if self.should_stop or self.successful_runs >= threads:
                        break
                    t = threading.Thread(target=self.thread_worker,
                                         args=(i + 1, ))
                    t.daemon = True
                    thread_list.append(t)
                    t.start()
                for t in thread_list:
                    t.join(
                        timeout=max(0, self._timeout -
                                    (time.time() - start_time)))
                if time.time() - start_time > self._timeout:
                    print(
                        f"{Fore.RED}⚠️ Thread {cycle_count} failed, trying to the next thread.{Style.RESET_ALL}"
                    )
            print(
                f"{Fore.GREEN}✅ Hoàn thành! Đã gửi {self.successful_runs} tin nhắn thành công.{Style.RESET_ALL}"
            )
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}Stopping all threads...{Style.RESET_ALL}")
            self.should_stop = True
            print(
                f"{Fore.GREEN}Completed {self.successful_runs} questions before stopping.{Style.RESET_ALL}"
            )
        finally:
            self.should_stop = True
            printer_thread.join(timeout=1.0)


if __name__ == "__main__":
    init()
    ngl = zNGL()
    ngl.banner()
    ngl.run(ngl._username, ngl._threads, ngl._question)
