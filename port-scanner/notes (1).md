# Port Scanner: Concepts Notes

## Socket concepts

### How the socket scanner works
- Uses Python's built-in `socket` module to attempt a raw TCP connection to each port on the target host.
- `socket.connect_ex((host, port))` attempts the connection and returns an integer instead of raising an exception — `0` means the port is open; any other value means it's closed or filtered.
- `socket.settimeout(n)` caps how long the program waits on a single unresponsive port, so the scan doesn't hang indefinitely.
- Ports are scanned **one at a time, in sequence** — the program fully waits for each connection attempt to resolve before starting the next.

### Why it's slow
- Port scanning is I/O-bound: almost all the time is spent waiting for the OS/network to respond, not doing any actual computation.
- Doing this sequentially means the CPU sits idle for the vast majority of the scan. Scanning 1,000 ports at a 0.5s timeout each could take 8+ minutes in the worst case, even though there's barely any real work happening.
- This bottleneck — waiting, not computing — is exactly what concurrency (threading/asyncio) is built to fix.

### Key takeaway
This version exists to prove the raw mechanics of a TCP connect scan before adding any concurrency on top.

## Threading concepts

### Why threading?
- Since scanning is I/O-bound, many connection attempts can happen *at the same time* instead of one after another — while one thread is waiting on a response, another can be actively attempting a different port.
- Python's `threading` module spins up multiple threads, each independently attempting a connection to a different port.

### Core components
- `threading.Thread` — creates a new thread that runs the port-check function independently of the main program.
- `queue.Queue` — a thread-safe structure that hands out ports to worker threads one at a time. Each thread pulls a port, scans it, and goes back for the next — this avoids two threads accidentally scanning the same port or needing manual locking to divide the work.
- A **fixed pool** of worker threads (e.g. 50–100) is used instead of one thread per port — spawning thousands of OS threads has its own overhead and can slow the scan down or crash it.

### The GIL caveat
- Python's Global Interpreter Lock (GIL) means only one thread executes Python bytecode at a time — threading in Python does **not** give true CPU parallelism.
- This doesn't hurt a port scanner because the threads spend almost all their time *waiting* on network I/O, not running Python code. While one thread is blocked on a socket call, the GIL is released and another thread runs. So threading is still a genuine speedup for I/O-bound work like this — just not for CPU-heavy work.

### Key takeaway
Threading turns a sequential, wait-heavy scan into a concurrent one — the GIL doesn't matter here because the bottleneck was always network latency, never the CPU.

## Asyncio concepts

### Why asyncio?
Threading creates multiple OS threads to perform work concurrently. `asyncio` instead uses an **event loop** to manage many asynchronous tasks, allowing the program to efficiently handle lots of I/O operations without creating a thread for every operation. This is especially useful for network programs because most of the time is spent **waiting for network responses**.

**Without concurrency:** each port is scanned one at a time, and the program is fully blocked while waiting for every single connection attempt to finish.

**With threading:** multiple OS threads run "concurrently," but each individual thread still fully blocks while waiting on its own connection — the OS is just switching between threads to create the illusion of simultaneity.

**With asyncio:** a single thread runs an event loop that juggles many coroutines. When a coroutine hits an `await` (e.g. waiting on a connection), it yields control straight back to the event loop, which immediately finds another coroutine to run instead of sitting idle. Nothing is ever truly blocked — so far more connection attempts can be "in flight" at once than a thread-per-connection model could manage.

### Core components
- `async def` — defines a coroutine function instead of a regular function.
- `await` — pauses the coroutine at an I/O point and hands control back to the event loop until that operation completes.
- `asyncio.open_connection(host, port)` — the asyncio equivalent of `socket.connect_ex()`; attempts a connection without blocking the whole program.
- `asyncio.wait_for(coro, timeout)` — the asyncio equivalent of `socket.settimeout()`, so one stuck connection can't hang the entire scan.
- `asyncio.gather(*tasks)` — runs many coroutines concurrently and waits for all of them to complete.

### Threading vs. asyncio — which is actually faster?
- For a pure port scanner (short-lived, I/O-bound connections), asyncio is usually faster and lighter at scale — an event loop juggling thousands of coroutines has far less overhead than the OS managing thousands of threads (each OS thread carries real memory and context-switching cost that a coroutine doesn't).
- Threading is easier to reason about for smaller scans since the code reads more like normal sequential code.
- Asyncio scales better for large port ranges or large IP ranges, which is why most modern, high-performance scanners lean on async I/O under the hood.

### Key takeaway
Asyncio solves the same core problem as threading — don't sit idle waiting on I/O — but does it with one thread and cooperative multitasking instead of many OS threads, which is why it tends to win as the scan gets bigger.

## Quick comparison

| Approach | Concurrency model | Best for | Main limitation |
|---|---|---|---|
| Basic socket | None (sequential) | Understanding the raw mechanics | Very slow at scale |
| Threading | Multiple OS threads | Small–medium scans, simpler mental model | Thread overhead at large scale |
| Asyncio | Single-threaded event loop | Large scans, many concurrent connections | More complex to reason about/debug |
