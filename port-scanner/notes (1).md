# 📝 Notes — Port Scanner

Personal notes written while building both versions of this tool.

---

## Core concept — what is a port scan?

A TCP port scanner tries to complete a TCP handshake with every port on a target.

Normal TCP connection (3-way handshake):
```
Client  →  SYN        →  Server
Client  ←  SYN-ACK    ←  Server   (port is OPEN)
Client  →  ACK        →  Server
```

If no SYN-ACK comes back — port is CLOSED or FILTERED.

A port scanner just automates this for every port number (1–65535).

---

## socket module

`socket` is Python's built-in networking library. It lets you open raw network connections.

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Breaking this down:
- `socket.AF_INET` — use IPv4 addresses (like 192.168.1.1)
- `socket.SOCK_STREAM` — use TCP (reliable, connection-based)
- If you wanted UDP you'd use `SOCK_DGRAM` instead

---

## connect_ex() vs connect()

Two ways to attempt a connection:

```python
sock.connect((host, port))      # throws exception if fails — bad for scanning
sock.connect_ex((host, port))   # returns 0 if open, non-zero if closed — good for scanning
```

Always use `connect_ex()` in a scanner because you EXPECT most ports to fail — you don't want an exception every time.

Return values of `connect_ex()`:
- `0` = connection successful = port is OPEN
- anything else = connection failed = port is CLOSED or filtered

---

## settimeout()

```python
sock.settimeout(1)   # wait max 1 second before giving up
```

Without this: scanner hangs for a very long time on filtered ports (firewall drops the packet silently, no response ever comes).

With this: moves on after 1 second. Adjust lower (0.5) for speed, higher for accuracy on slow networks.

---

## gethostbyname()

Converts a hostname to an IP address:

```python
ip = socket.gethostbyname("scanme.nmap.org")
# returns "45.33.32.156"
```

Wrap in try/except because it throws `socket.gaierror` if hostname can't be resolved.

---

## Threading concepts (advanced version)

### Why threading?
Without threading: scan port 1 → wait → scan port 2 → wait → ... very slow
With threading: 100 workers each scanning a different port simultaneously → fast

### threading.Thread
```python
t = threading.Thread(target=function, args=(arg1, arg2))
t.start()   # starts the thread running
t.join()    # waits for thread to finish before continuing
```

### t.daemon = True
```python
t.daemon = True
```
If the main program exits (e.g. you press Ctrl+C), daemon threads die automatically.
Without this: threads keep running in the background even after the program "ends".

### Queue — the ticket dispenser
```python
from queue import Queue

queue = Queue()
queue.put(80)       # add port 80 to queue
queue.put(443)      # add port 443 to queue

port = queue.get()  # grab next item (80)
queue.task_done()   # tell queue I finished with this item
```

Every thread calls `queue.get()` to grab its next port. Queue handles the coordination — two threads never grab the same port.

Always call `queue.task_done()` after finishing each item. Use `finally` to make sure it runs even if an error happens:

```python
try:
    # do the scan
    pass
finally:
    queue.task_done()   # always runs, even on error
```

### threading.Lock
Problem without lock:
```
Thread 1: print("[OPEN] Port
Thread 2: print("[OPEN] Port      ← interrupts mid-line
Thread 1: 80 | HTTP")
```
Output becomes garbled.

Solution:
```python
print_lock = threading.Lock()

with print_lock:
    print(f"[OPEN] Port {port}")   # only one thread prints at a time
```

`with print_lock:` automatically acquires and releases the lock.

---

## Things I got wrong first time

- Forgot `sock.close()` after each scan — ran out of available sockets
- Forgot `queue.task_done()` — program hung at the end waiting forever
- Didn't use `with print_lock:` — output was jumbled with multiple threads
- Set timeout too high (3 seconds) — scan was still slow even with threads
- Forgot `t.join()` — program printed summary before threads finished scanning

---

## Common port numbers to memorise

```
21   FTP        (file transfer)
22   SSH        (secure remote access)
23   Telnet     (insecure remote access — red flag if open)
25   SMTP       (email sending)
53   DNS        (domain name resolution)
80   HTTP       (websites)
443  HTTPS      (secure websites)
445  SMB        (Windows file sharing — common attack target)
3306 MySQL      (database)
3389 RDP        (Windows remote desktop — common attack target)
```

---

## Connection to Nmap

Nmap's `-sT` flag is a TCP connect scan — exactly what this tool does.
Nmap's `-sS` (SYN scan) sends only the SYN packet and listens for SYN-ACK without completing the handshake — stealthier but requires root/admin.

This tool does a full connect scan (like `-sT`) because completing the handshake doesn't require special privileges.

---

## Resources
- Python socket docs: docs.python.org/3/library/socket.html
- Python threading docs: docs.python.org/3/library/threading.html
- Nmap port scanning techniques: nmap.org/book/man-port-scanning-techniques.html
