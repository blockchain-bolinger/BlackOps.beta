#!/usr/bin/env python3
"""
Network Scanner – Schnelle Port-Scans für Tools
"""
import os
import socket
from concurrent.futures import ThreadPoolExecutor

class NetworkScanner:
    def __init__(self, timeout=1):
        self.timeout = timeout

    def scan_port(self, host: str, port: int) -> dict:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return {'port': port, 'state': 'open' if result == 0 else 'closed'}

    def scan_ports(self, host: str, ports: list, threads=50) -> list:
        results = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.scan_port, host, p) for p in ports]
            for f in futures:
                results.append(f.result())
        return results

    def run(self):
        if os.environ.get("BLACKOPS_SELF_TEST") == "1":
            print("[SELF-TEST] NetworkScanner gestartet.")
            return
        host = input("Host/IP: ").strip()
        if not host:
            print("Abbruch.")
            return
        ports_raw = input("Ports (z.B. 22,80,443 oder 1-1000) [22,80,443]: ").strip()
        if not ports_raw:
            ports = [22, 80, 443]
        elif "-" in ports_raw:
            start, end = ports_raw.split("-", 1)
            ports = list(range(int(start), int(end) + 1))
        else:
            ports = [int(p.strip()) for p in ports_raw.split(",") if p.strip()]
        try:
            threads_raw = input("Threads [50]: ").strip()
            threads = int(threads_raw) if threads_raw else 50
        except ValueError:
            threads = 50

        results = self.scan_ports(host, ports, threads=threads)
        print("\n--- Scan Results ---")
        for r in results:
            print(f"{host}:{r['port']} -> {r['state']}")
        input("\n[ENTER] Zurueck...")
