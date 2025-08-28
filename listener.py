#!/usr/bin/env python3
# InzelSec - Reverse Shell Listener
# Description: listens on a TCP port, accepts a connection and interacts like a reverse netcat session.
#
# Usage:
#   python3 listener.py            # listens on 4444
#   python3 listener.py 9001       # listens on 9001
#   [Optional] type "exit" to close session

import socket
import argparse
import shutil
import sys
import os

# === Colors ===
GREEN  = "\033[0;32m"
RED    = "\033[0;31m"
YELLOW = "\033[1;33m"
NC     = "\033[0m"

# === Banner (mantém seu estilo) ===
def banner_inzelsec():
    width = shutil.get_terminal_size((80, 20)).columns
    line = "=" * width
    print(f"\n{NC}{line}{NC}")
    try:
        if shutil.which("figlet"):
            output = os.popen('figlet "InzelSec"').read()
        elif shutil.which("toilet") and os.path.exists(os.path.expanduser("~/.toilet/fonts/big.tlf")):
            output = os.popen('toilet -d ~/.toilet/fonts -f big -F metal "INZELSEC"').read()
        elif shutil.which("toilet"):
            output = os.popen('toilet -f standard -F metal "INZELSEC"').read()
        else:
            output = "InzelSec"
        for line_str in output.splitlines():
            pad = max((width - len(line_str)) // 2, 0)
            print(" " * pad + line_str)
    except Exception:
        print("InzelSec".center(width))
    print(f"{NC}{line}{NC}\n")

# === argparse colorido ===
import argparse
class ColorArgParser(argparse.ArgumentParser):
    def print_usage(self, file=None):
        text = self.format_usage()
        if file is None:
            print(f"{YELLOW}{text}{NC}", end="")
        else:
            file.write(f"{YELLOW}{text}{NC}")
    def print_help(self):
        text = self.format_help()
        print(f"{YELLOW}{text}{NC}", end="")
    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write(f"{RED}error: {message}{NC}\n")
        self.exit(2)

# === Listener ===
def start_listener(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", port))
            server.listen(1)
            print(f"{GREEN}[+] Listening on 0.0.0.0:{port}{NC}")

            # aguarda conexão, mas trata Ctrl+C de forma limpa
            try:
                conn, addr = server.accept()
            except KeyboardInterrupt:
                print(f"\n{YELLOW}[*] Listener stopped (no client connected).{NC}")
                return

            print(f"{GREEN}[+] Connection received from {addr[0]}:{addr[1]}{NC}")

            with conn:
                while True:
                    try:
                        cmd = input("Shell> ")
                        if cmd.strip().lower() == "exit":
                            try:
                                conn.send(b"exit\n")
                            except Exception:
                                pass
                            print(f"{YELLOW}[*] Session closed.{NC}")
                            break

                        conn.sendall((cmd + "\n").encode())
                        resp = conn.recv(4096)
                        if not resp:
                            print(f"{RED}[-] Client closed the connection.{NC}")
                            break
                        print(resp.decode(), end="")

                    except KeyboardInterrupt:
                        print(f"\n{YELLOW}[*] Session interrupted by user.{NC}")
                        break

    except OSError as e:
        if e.errno == 98 or "Address already in use" in str(e):
            print(f"{RED}[-] Error: address already in use on port {port}.{NC}")
            print(f"{YELLOW}[*] Tip: close the previous listener or pick another port.{NC}")
        else:
            print(f"{RED}[-] Error: {e}{NC}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}[-] Error: {e}{NC}")
        sys.exit(1)

# === Main ===
if __name__ == "__main__":
    banner_inzelsec()

    parser = ColorArgParser(
        description="InzelSec - Reverse Shell Listener (positional PORT; defaults to 4444)",
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("port", nargs="?", type=int, default=4444,
                        help="Port to listen on (default: 4444)")
    args = parser.parse_args()

    start_listener(args.port)
