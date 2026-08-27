import asyncio
import time


MAX_CONCURRENT = 100
CONNECTION_TIMEOUT = 0.5
BANNER_TIMEOUT = 0.3

sem = asyncio.Semaphore(MAX_CONCURRENT)

open_ports = []

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
async def get_banner(reader):
    try:
        data = await asyncio.wait_for(
            reader.read(1024),
            timeout=BANNER_TIMEOUT
        )
        if data:
            return data.decode(
                errors="replace"
            ).strip()
    except asyncio.TimeoutError:
        pass
    return None

async def http_probe(host, reader, writer):
    request = (
        f"HEAD / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    try:
        writer.write(request.encode())
        await writer.drain()
        response = await asyncio.wait_for(
            reader.read(4096),
            timeout=0.5
        )
        return response.decode(
            errors="replace"
        )
    except asyncio.TimeoutError:
        return None

def parse_http_response(response):

    if not response:
        return None, None, None
    lines = response.split("\r\n")
    status = None
    server = None
    content_type = None

    if lines:
        parts = lines[0].split(" ")
        if len(parts) >= 2:
            status = parts[1]

    for line in lines:
        if line.lower().startswith("server:"):
            server = line.split(":", 1)[1].strip()
        elif line.lower().startswith("content-type:"):
            content_type = line.split(":", 1)[1].strip()
    return status, server, content_type

async def scanner(host, queue):
    while True:
        port = await queue.get()
        if port is None:
            queue.task_done()
            break
        try:
            async with sem:
                try:
                    reader, writer = await asyncio.wait_for(
                        asyncio.open_connection(
                            host,
                            port
                        ),
                        timeout=CONNECTION_TIMEOUT
                    )
                    service = COMMON_PORTS.get(
                        port,
                        "Unknown"
                    )
                    banner = None

                    if port in (80, 8080, 8000, 8081):
                        response = await http_probe(
                            host,
                            reader,
                            writer
                        )
                        status, server, content_type = (
                            parse_http_response(response)
                        )
                        print(
                            f"[+] Port {port} OPEN | "
                            f"HTTP | "
                            f"Status: {status} | "
                            f"Server: {server} | "
                            f"Content-Type: {content_type}"
                        )
                        banner = response[:200] if response else None
                    else:
                        banner = await get_banner(
                            reader
                        )
                        print(
                            f"[+] Port {port} OPEN | "
                            f"{service} | "
                            f"{banner if banner else 'No banner'}"
                        )
                    open_ports.append(
                        (port, service, banner) )
                    writer.close()
                    await writer.wait_closed()
                except asyncio.TimeoutError:
                    pass
                except ConnectionRefusedError:
                    pass
                except OSError:
                    pass
        finally:
            queue.task_done()

async def main():
    host = input("Enter target: ")
    start_port = int(
        input("Starting port: ") )
    end_port = int(
        input("Ending port: ") )
    queue = asyncio.Queue()

    for port in range(
        start_port,
        end_port + 1):
        await queue.put(port)

    start_time = time.perf_counter()
    workers = []
    for _ in range(MAX_CONCURRENT):
        worker = asyncio.create_task(
            scanner(host, queue)   )
        workers.append(worker)
    await queue.join()

    for _ in range(MAX_CONCURRENT):
        await queue.put(None)
    await asyncio.gather(*workers)

    end_time = time.perf_counter()

    print("\n========== SCAN COMPLETE ==========")
    print("\nOpen ports:")

    for port, service, banner in sorted(
        open_ports):
        print(
            f"Port {port}: "
            f"{service} | "
            f"{banner if banner else 'No banner'}")
    print(
        f"\nTime taken: "
        f"{end_time - start_time:.2f} seconds")

asyncio.run(main())
