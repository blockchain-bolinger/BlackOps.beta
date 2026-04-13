#!/usr/bin/env python3
"""
File Analyzer – Dateianalyse-Tool
"""
import os
import hashlib
try:
    import magic
except ImportError:
    magic = None

class FileAnalyzer:
    @staticmethod
    def get_hash(file_path: str, algo='sha256') -> str:
        h = hashlib.new(algo)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def get_mime(file_path: str) -> str:
        if magic is None:
            return "unknown (python-magic missing)"
        return magic.from_file(file_path, mime=True)

    @staticmethod
    def get_size(file_path: str) -> int:
        return os.path.getsize(file_path)

    @staticmethod
    def is_executable(file_path: str) -> bool:
        return os.access(file_path, os.X_OK)

    def run(self):
        if os.environ.get("BLACKOPS_SELF_TEST") == "1":
            print("[SELF-TEST] FileAnalyzer gestartet.")
            return
        path = input("Datei-Pfad: ").strip().strip("'")
        if not path:
            print("Abbruch.")
            return
        if not os.path.exists(path):
            print("Datei existiert nicht.")
            return
        try:
            size = self.get_size(path)
            mime = self.get_mime(path)
            sha256 = self.get_hash(path, "sha256")
            md5 = self.get_hash(path, "md5")
            is_exec = self.is_executable(path)
            print("\n--- File Analyzer ---")
            print(f"Pfad: {path}")
            print(f"Size: {size} bytes")
            print(f"MIME: {mime}")
            print(f"SHA256: {sha256}")
            print(f"MD5: {md5}")
            print(f"Executable: {is_exec}")
        except Exception as e:
            print(f"Fehler: {e}")
        input("\n[ENTER] Zurueck...")
