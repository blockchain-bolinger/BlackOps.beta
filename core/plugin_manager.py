#!/usr/bin/env python3
import importlib
import pkgutil
import inspect
import os
import sys

class PluginInterface:
    """Jedes Plugin MUSS dieses Interface implementieren."""
    def name(self):
        raise NotImplementedError

    def description(self):
        return ""

    def run(self, **kwargs):
        raise NotImplementedError

class PluginManager:
    """Lädt alle Plugins aus dem Ordner tools/plugins/."""

    def __init__(self, plugin_dir="tools/plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def discover(self):
        """Durchsucht den Plugin-Ordner nach gültigen Plugins."""
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            open(os.path.join(self.plugin_dir, "__init__.py"), "a").close()
            print(f"[*] Plugin-Ordner {self.plugin_dir} erstellt.")

        plugins = {}
        # Füge Plugin-Ordner zum Python-Pfad hinzu
        sys.path.insert(0, os.path.dirname(self.plugin_dir))

        for finder, name, ispkg in pkgutil.iter_modules([self.plugin_dir]):
            if ispkg:
                try:
                    module = importlib.import_module(f"tools.plugins.{name}.plugin")
                    for cls_name, cls in inspect.getmembers(module, inspect.isclass):
                        if issubclass(cls, PluginInterface) and cls is not PluginInterface:
                            instance = cls()
                            plugins[name] = instance
                            print(f"[+] Plugin geladen: {name}")
                except Exception as e:
                    print(f"[-] Fehler beim Laden von Plugin {name}: {e}")

        self.plugins = plugins
        return plugins

    def get_plugin(self, name):
        return self.plugins.get(name)

    def list_plugins(self):
        return list(self.plugins.keys())