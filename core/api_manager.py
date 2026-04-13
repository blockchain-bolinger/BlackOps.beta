#!/usr/bin/env python3
import json
import os

class APIManager:
    """Verwaltet API-Schlüssel aus secrets.json."""

    def __init__(self, secrets_file="secrets.json"):
        self.secrets_file = secrets_file
        self.keys = self._load_keys()

    def _load_keys(self):
        if not os.path.exists(self.secrets_file):
            print(f"[!] {self.secrets_file} nicht gefunden. Bitte anlegen.")
            return {}
        with open(self.secrets_file, "r") as f:
            return json.load(f)

    def get(self, service):
        """Gibt den API-Key für einen Dienst zurück."""
        return self.keys.get(service, {}).get("api_key")

    def set(self, service, api_key):
        """Speichert einen API-Key (optional)."""
        if service not in self.keys:
            self.keys[service] = {}
        self.keys[service]["api_key"] = api_key
        with open(self.secrets_file, "w") as f:
            json.dump(self.keys, f, indent=2)