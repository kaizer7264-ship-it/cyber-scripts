#!/usr/bin/env python3
# port_scanner.py — simple TCP port scanner (educational)
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

def scan_port(host, port, timeout=1.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return port if result == 0 else None
    except Exception:
        return None

def scan_range(host, start, end, workers=100, timeout=1.0):
    open_ports = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(scan_port, host, p, timeout): p for p in range(start, end + 1)}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                open_ports.append(res)
    return sorted(open_ports)

def main():
    parser = argparse.ArgumentParser(description="Simple TCP port scanner (use on authorized targets only).")
    parser.add_argument("host", help="Target host (IP or hostname)")
    parser.add_argument("--start", type=int, default=1, help="Start port (default 1)")
    parser.add_argument("--end", type=int, default=1024, help="End port (default 1024)")
    parser.add_argument("--workers", type=int, default=200, help="Concurrent threads (default 200)")
    parser.add_argument("--timeout", type=float, default=0.6, help="Socket timeout seconds (default 0.6)")
    args = parser.parse_args()

    target = args.host
    start = max(1, args.start)
    end = min(65535, args.end)

    print(f"Scanning {target} ports {start}-{end} with {args.workers} workers (timeout {args.timeout}s)")
    t0 = datetime.now()
    open_ports = scan_range(target, start, end, workers=args.workers, timeout=args.timeout)
    t1 = datetime.now()
    delta = (t1 - t0).total_seconds()

    if open_ports:
        print(f"\nOpen ports on {target}: {', '.join(map(str, open_ports))}")
    else:
        print(f"\nNo open ports found in range {start}-{end} on {target}")

    print(f"\nScan completed in {delta:.2f} seconds")

if __name__ == "__main__":
    main()
