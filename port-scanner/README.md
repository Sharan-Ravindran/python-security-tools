# 🔍 Python Port Scanner

A TCP port scanner built from scratch in Python to understand how
network scanning works and how concurrency can improve performance.

This project contains **three versions of the same core scanner**:

1. **Socket Scanner** — sequential TCP scanning
2. **Threaded Scanner** — concurrent scanning using threads
3. **Asyncio Scanner** — asynchronous scanning using Python's asyncio framework

The scanners were built progressively so I could understand the
underlying concepts rather than immediately relying on a high-level
tool.

> ⚠️ Only scan systems you own or have explicit permission to test.

---

# 📁 Project Structure

```text
Port-Scanner/
│
├── README.md
│
├── socket_scanner/
│   └── socket_scanner.py
│
├── threaded_scanner/
│   └── threaded_scanner.py
│
└── asyncio_scanner/
    └── asyncio_scanner.py
