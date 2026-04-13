"""
Advanced Logging System für Black Ops Framework
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import colorama
from colorama import Fore, Style

colorama.init()

class BlackOpsLogger:
    def __init__(self, name: str = "BlackOps", log_dir: str = "logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup Logging
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console Handler mit Farben
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter()
        console_handler.setFormatter(console_formatter)
        
        # File Handler
        log_file = self.log_dir / f"blackops_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = None
        try:
            file_handler = logging.FileHandler(log_file)
        except PermissionError:
            fallback = self.log_dir / f"blackops_user_{datetime.now().strftime('%Y%m%d')}.log"
            try:
                file_handler = logging.FileHandler(fallback)
            except PermissionError:
                file_handler = None

        if file_handler:
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
        
        # Handlers hinzufügen
        self.logger.addHandler(console_handler)
        if file_handler:
            self.logger.addHandler(file_handler)
        
        # Audit Logger
        self.audit_logger = self._setup_audit_logger()
    
    def _setup_audit_logger(self) -> logging.Logger:
        """Setup für Audit-Logging"""
        audit_logger = logging.getLogger(f"{self.name}.audit")
        audit_logger.setLevel(logging.INFO)
        
        audit_dir = self.log_dir / "audit"
        audit_dir.mkdir(exist_ok=True)
        
        audit_file = audit_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
        audit_handler = None
        try:
            audit_handler = logging.FileHandler(audit_file)
        except PermissionError:
            fallback = audit_dir / f"audit_user_{datetime.now().strftime('%Y%m%d')}.log"
            try:
                audit_handler = logging.FileHandler(fallback)
            except PermissionError:
                audit_handler = None

        if audit_handler:
            audit_handler.setLevel(logging.INFO)
            audit_formatter = logging.Formatter(
                '%(asctime)s - %(user)s - %(action)s - %(target)s - %(status)s'
            )
            audit_handler.setFormatter(audit_formatter)
            audit_logger.addHandler(audit_handler)
        return audit_logger
    
    def info(self, message: str) -> None:
        """Informations-Log"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Warnungs-Log"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Fehler-Log"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Kritischer Fehler"""
        self.logger.critical(message)
    
    def debug(self, message: str) -> None:
        """Debug-Log"""
        self.logger.debug(message)
    
    def audit(self, user: str, action: str, target: str, status: str = "SUCCESS") -> None:
        """Audit-Log für Sicherheitsrelevante Aktionen"""
        extra = {'user': user, 'action': action, 'target': target, 'status': status}
        self.audit_logger.info("", extra=extra)
    
    def print_banner(self) -> None:
        """Framework Banner"""
        banner = f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗ ███████╗║
║      ██╔══██╗██║     ██╔══██╗██╔════╝██║  ██║██╔══██╗██╔════╝║
║      ██████╔╝██║     ███████║██║     ███████║██████╔╝███████╗║
║      ██╔══██╗██║     ██╔══██║██║     ██╔══██║██╔═══╝ ╚════██║║
║      ██████╔╝███████╗██║  ██║╚██████╗██║  ██║██║     ███████║║
║      ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝║
║                                                              ║
║                   FRAMEWORK v2.2                             ║
║              FOR ETHICAL SECURITY RESEARCH                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)

class ColoredFormatter(logging.Formatter):
    """Custom Formatter mit Farben"""
    
    FORMATS = {
        logging.DEBUG: Fore.CYAN + "[DEBUG] %(message)s" + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + "[INFO] %(message)s" + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + "[WARNING] %(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + "[ERROR] %(message)s" + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + "[CRITICAL] %(message)s" + Style.RESET_ALL,
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
