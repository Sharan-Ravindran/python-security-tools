# 🔍 Port Scanner

A TCP port scanner built in Python. Comes in two versions — basic (single threaded) and advanced (multithreaded) — built in that order to understand the concepts before optimising.

This tool does what Nmap does at its core: attempts TCP connections to each port on a target and reports which ones are open.

---

## Versions

### basic/port_scanner.py
- Scans one port at a time
- Simple and easy to read — every line is understandable
- Slow on large ranges (each port waits 1 second to timeout)
- Good for understanding how port scanning works at the code level

### advanced/port_scanner_threaded.py
- Scans up to 100 ports simultaneously using threads
- Significantly faster — same 1024 ports in seconds instead of minutes
- Uses `Queue` to safely distribute work across threads
- Uses a `Lock` to prevent garbled output when multiple threads print at once

---

## How to run

```bash
# Basic version
python basic/port_scanner.py

# Threaded version
python advanced/port_scanner_threaded.py
```

No external libraries needed — uses only Python built-in modules (`socket`, `threading`, `queue`, `datetime`).

---

## Example output

```
==================================================
     PYTHON PORT SCANNER  (threaded)
==================================================

Enter target IP or hostname: scanme.nmap.org

Target  : scanme.nmap.org (45.33.32.156)
Range   : 1 - 1024
Threads : 100
Started : 14:32:01
--------------------------------------------------
[OPEN]  Port    22  |  SSH
[OPEN]  Port    80  |  HTTP
--------------------------------------------------
Finished  : 14:32:09
Duration  : 8 seconds
Open ports: 2
Found     : [22, 80]
```

---

## Legal targets for testing

| Target | Notes |
|--------|-------|
| `localhost` | Your own machine — always fine |
| `scanme.nmap.org` | Nmap's official practice server — legally open for scanning |
| Your own VM | VirtualBox / VMware — fine |

**Never scan an IP you don't own or have permission to scan.**

---

## What I learned building this

- How TCP connections work — a port scanner is just trying to complete a handshake
- The `socket` module — Python's interface to network connections
- Why `connect_ex()` is better than `connect()` for scanning — returns error codes instead of throwing exceptions
- Why `settimeout()` is essential — without it the scanner hangs forever on filtered ports
- How threading works — one worker per thread, all running at the same time
- Why a `Lock` is needed — multiple threads printing simultaneously produces garbled output
- How `Queue` distributes work safely across threads — like a ticket dispenser
- The difference between `t.join()` and `t.daemon = True`

---

## Speed comparison

| Version | Ports scanned | Time (approx) |
|---------|--------------|---------------|
| Basic | 1–1024 | 8–15 minutes |
| Threaded (100 workers) | 1–1024 | 8–15 seconds |

---

## Concepts used

| Concept | File |
|---------|------|
| `socket.socket()` | Both |
| `connect_ex()` | Both |
| `settimeout()` | Both |
| `gethostbyname()` | Both |
| Dictionary `.get()` | Both |
| `threading.Thread` | Advanced |
| `threading.Lock` | Advanced |
| `queue.Queue` | Advanced |
| `t.join()` | Advanced |
| `t.daemon = True` | Advanced |

---

## Connection to internship work

The first phase of my internship pentest was reconnaissance — running Nmap to find open ports and services. Building this tool from scratch showed me exactly what Nmap is doing when it runs a TCP connect scan (`-sT` flag). Understanding the tool at this level makes me better at interpreting its output and explaining findings in a report.
