import socket
from datetime import datetime

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt"
}

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False

def get_hostname(host):
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        print("Could not resolve hostname.")
        return None
print("=" * 50)
print("         PYTHON PORT SCANNER")
print("=" * 50)
target = input("\nEnter target IP or hostname: ")
ip = get_hostname(target)
if not ip:
    exit()

print("\nScan options:")
print("1. Common ports only (1-1024)")
print("2. Custom range")
choice = int(input("Choose (1 or 2): "))

if choice == 1:
    start_port, end_port = 1, 1024
elif choice == 2:
    start_port = int(input("Start port: "))
    end_port   = int(input("End port: "))
else:
    start_port, end_port = 1, 1024

print(f"\nTarget   : {target} ({ip})")
print(f"Range    : {start_port} - {end_port}")
print(f"Started  : {datetime.now().strftime('%H:%M:%S')}")
print("-" * 50)

open_ports = []

for port in range(start_port, end_port + 1):
    if scan_port(ip, port):
        service = COMMON_PORTS.get(port, "Unknown")
        print(f"[OPEN]  Port {port:5}  |  {service}")
        open_ports.append(port)
print("-" * 50)
print(f"Scan finished : {datetime.now().strftime('%H:%M:%S')}")
print(f"Open ports    : {len(open_ports)}")
if open_ports:
    print(f"Ports found   : {open_ports}")
