import socket
import threading
from queue import Queue
from datetime import datetime

THREADS = 100        
TIMEOUT = 0.5        

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
open_ports = []
print_lock = threading.Lock()

def scan_worker(host, queue):
    while not queue.empty():
        port = queue.get()   

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)
            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")

                with print_lock:
                    print(f"[OPEN]  Port {port:5}  |  {service}")
                    open_ports.append(port)

        except socket.error:
            pass

        finally:
            queue.task_done()  

print("=" * 50)
print("     PYTHON PORT SCANNER  (threaded)")
print("=" * 50)

target = input("\nEnter target IP or hostname: ")

try:
    ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Could not resolve hostname.")
    exit()

print("\nScan options:")
print("1. Common ports (1-1024)")
print("2. Custom range")
choice = input("Choose (1 or 2): ")

if choice == "1":
    start_port, end_port = 1, 1024
elif choice == "2":
    start_port = int(input("Start port: "))
    end_port   = int(input("End port: "))
else:
    start_port, end_port = 1, 1024

print(f"\nTarget  : {target} ({ip})")
print(f"Range   : {start_port} - {end_port}")
print(f"Threads : {THREADS}")
print(f"Started : {datetime.now().strftime('%H:%M:%S')}")
print("-" * 50)

start_time = datetime.now()

queue = Queue()
for port in range(start_port, end_port + 1):
    queue.put(port)


threads = []
for _ in range(THREADS):
    t = threading.Thread(target=scan_worker, args=(ip, queue))
    t.daemon = True    
    t.start()
    threads.append(t)

for t in threads:
    t.join()

end_time = datetime.now()
duration = (end_time - start_time).seconds

print("-" * 50)
print(f"Finished  : {end_time.strftime('%H:%M:%S')}")
print(f"Duration  : {duration} seconds")
print(f"Open ports: {len(open_ports)}")
if open_ports:
    print(f"Found     : {sorted(open_ports)}")
