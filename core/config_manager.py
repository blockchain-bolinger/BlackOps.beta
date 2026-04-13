"""
Configuration Manager für Black Ops Framework
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

class ConfigManager:
    def __init__(self, config_path: str = "blackops_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Lädt die Konfiguration aus JSON oder YAML"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                if self.config_path.suffix == '.json':
                    return json.load(f)
                elif self.config_path.suffix in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
        
        # Default-Konfiguration
        return {
            "version": "2.2.0",
            "debug": False,
            "log_level": "INFO",
            "encryption": {
                "algorithm": "AES-256-GCM",
                "key_rotation_days": 30
            },
            "network": {
                "timeout": 30,
                "max_retries": 3,
                "proxy": None
            },
            "ethics": {
                "allowed_targets": [],
                "forbidden_actions": [],
                "require_approval": True
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Holt Wert aus Konfiguration"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Setzt Wert in Konfiguration"""
        keys = key.split('.')
        config_ref = self.config
        
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        config_ref[keys[-1]] = value
        self._save_config()
    
    def _save_config(self) -> None:
        """Speichert Konfiguration"""
        with open(self.config_path, 'w') as f:
            if self.config_path.suffix == '.json':
                json.dump(self.config, f, indent=2)
            elif self.config_path.suffix in ['.yaml', '.yml']:
                yaml.dump(self.config, f, default_flow_style=False)
    
    def validate(self) -> bool:
        """Validiert Konfiguration"""
        required_keys = ['version', 'ethics']
        
        for key in required_keys:
            if key not in self.config:
                return False
        
        # Ethics-Validierung
        if 'allowed_targets' not in self.config.get('ethics', {}):
            return False
        
        return True