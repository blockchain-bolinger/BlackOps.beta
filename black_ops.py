#!/usr/bin/env python3
"""
Black Ops Framework v2.2
Main Entry Point
"""

import sys
import argparse
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

from core.blackops_logger import BlackOpsLogger
from core.config_manager import ConfigManager
from core.ethics_enforcer import EthicsEnforcer
from core.session_manager import SessionManager

class BlackOpsFramework:
    def __init__(self):
        self.logger = BlackOpsLogger()
        self.config = ConfigManager()
        self.ethics = EthicsEnforcer()
        self.session = SessionManager()
        
    def run(self):
        """Hauptausführungsfunktion"""
        self.logger.print_banner()
        
        # Startup checks
        if not self._startup_checks():
            sys.exit(1)
        
        # Main menu
        self._show_main_menu()
    
    def _startup_checks(self) -> bool:
        """Führt Startup-Checks durch"""
        self.logger.info("Starting Black Ops Framework v2.2")
        
        # Check config
        if not self.config.validate():
            self.logger.error("Invalid configuration")
            return False
        
        # Check ethics agreement
        if not self._check_ethics_agreement():
            self.logger.error("Ethics agreement not accepted")
            return False
        
        # Check dependencies
        if not self._check_dependencies():
            self.logger.warning("Some dependencies missing")
        
        self.logger.info("Startup checks passed")
        return True
    
    def _check_ethics_agreement(self) -> bool:
        """Prüft Ethics Agreement"""
        agreement_path = Path("ethics_agreement.txt")
        
        if not agreement_path.exists():
            self.logger.warning("No ethics agreement found")
            
            print("\n" + "="*60)
            print("ETHICAL USE AGREEMENT")
            print("="*60)
            print("""
1. This framework is for authorized security testing only.
2. You must have written permission to test any system.
3. Do not use for illegal or unauthorized activities.
4. Respect privacy and data protection laws.
5. Report vulnerabilities responsibly.
            """)
            
            response = input("\nDo you agree to these terms? (yes/NO): ").strip().lower()
            
            if response == "yes":
                with open(agreement_path, 'w') as f:
                    f.write("Ethics Agreement Accepted\n")
                return True
            else:
                return False
        
        return True
    
    def _check_dependencies(self) -> bool:
        """Prüft Abhängigkeiten"""
        import importlib
        
        required = {
            'requests': 'requests',
            'cryptography': 'cryptography',
            'colorama': 'colorama',
            'dns': 'dnspython',
            'bs4': 'beautifulsoup4'
        }
        
        missing = []
        
        for module_name, package in required.items():
            try:
                importlib.import_module(module_name)
            except ImportError:
                missing.append(package)
        
        if missing:
            self.logger.warning(f"Missing packages: {', '.join(missing)}")
            print(f"\nInstall missing packages with:")
            print(f"pip install {' '.join(missing)}")
            
            return False
        
        return True
    
    def _show_main_menu(self):
        """Zeigt Hauptmenü"""
        while True:
            print("\n" + "="*60)
            print("BLACK OPS FRAMEWORK v2.2 - MAIN MENU")
            print("="*60)
            
            categories = {
                "1": "Reconnaissance Tools",
                "2": "Offensive Tools",
                "3": "Stealth Tools",
                "4": "Intelligence Tools",
                "5": "Utility Tools",
                "6": "Session Management",
                "7": "Configuration",
                "8": "Reports",
                "9": "Exit"
            }
            
            for key, value in categories.items():
                print(f"{key}. {value}")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self._show_recon_menu()
            elif choice == "2":
                self._show_offensive_menu()
            elif choice == "3":
                self._show_stealth_menu()
            elif choice == "4":
                self._show_intelligence_menu()
            elif choice == "5":
                self._show_utils_menu()
            elif choice == "6":
                self.session.manage()
            elif choice == "7":
                self._show_config_menu()
            elif choice == "8":
                self._show_reports_menu()
            elif choice == "9":
                self.logger.info("Exiting Black Ops Framework")
                break
            else:
                print("Invalid option")
    
    def _show_recon_menu(self):
        """Zeigt Reconnaissance Menü"""
        tools = {
            "1": "Social Hunter v7",
            "2": "NetScout Pro",
            "3": "MetaSpy",
            "4": "Back"
        }
        
        while True:
            print("\n--- RECONNAISSANCE TOOLS ---")
            for key, value in tools.items():
                print(f"{key}. {value}")
            
            choice = input("\nSelect tool: ").strip()
            
            if choice == "1":
                self._run_tool("tools.recon.social_hunter_v7:SocialHunterV7")
            elif choice == "2":
                self._run_tool("tools.recon.netscout_pro:NetScoutPro")
            elif choice == "3":
                self._run_tool("tools.recon.metaspy:MetaSpy")
            elif choice == "4":
                break
    
    def _show_offensive_menu(self):
        """Zeigt Offensive Tools Menü"""
        tools = {
            "1": "AirStrike",
            "2": "NetShark",
            "3": "Silent Phish",
            "4": "Venom Maker",
            "5": "HashBreaker",
            "6": "Back"
        }
        
        while True:
            print("\n--- OFFENSIVE TOOLS ---")
            for key, value in tools.items():
                print(f"{key}. {value}")
            
            choice = input("\nSelect tool: ").strip()
            
            if choice == "1":
                self._run_tool("tools.offensive.airstrike:AirStrike")
            elif choice == "2":
                self._run_tool("tools.offensive.netshark:NetShark")
            elif choice == "3":
                self._run_tool("tools.offensive.silent_phish:SilentPhish")
            elif choice == "4":
                self._run_tool("tools.offensive.venom_maker:VenomMaker")
            elif choice == "5":
                self._run_tool("tools.offensive.hashbreaker:HashBreaker")
            elif choice == "6":
                break
    
    def _show_stealth_menu(self):
        """Zeigt Stealth Tools Menü"""
        tools = {
            "1": "Ghost Net",
            "2": "Traceless",
            "3": "Back"
        }
        
        while True:
            print("\n--- STEALTH TOOLS ---")
            for key, value in tools.items():
                print(f"{key}. {value}")
            
            choice = input("\nSelect tool: ").strip()
            
            if choice == "1":
                self._run_tool("tools.stealth.ghost_net:GhostNet")
            elif choice == "2":
                self._run_tool("tools.stealth.traceless:Traceless")
            elif choice == "3":
                break
    
    def _show_intelligence_menu(self):
        """Zeigt Intelligence Menü"""
        tools = {
            "1": "NeuroLink",
            "2": "Back"
        }
        
        while True:
            print("\n--- INTELLIGENCE TOOLS ---")
            for key, value in tools.items():
                print(f"{key}. {value}")
            
            choice = input("\nSelect tool: ").strip()
            
            if choice == "1":
                self._run_tool("tools.intelligence.neurolink:NeuroLink")
            elif choice == "2":
                break
    
    def _show_utils_menu(self):
        """Zeigt Utility Menü"""
        tools = {
            "1": "CryptoVault",
            "2": "File Analyzer",
            "3": "Network Scanner",
            "4": "System Info",
            "5": "Back"
        }
        
        while True:
            print("\n--- UTILITY TOOLS ---")
            for key, value in tools.items():
                print(f"{key}. {value}")
            
            choice = input("\nSelect tool: ").strip()
            
            if choice == "1":
                self._run_tool("tools.utils.cryptovault:CryptoVault")
            elif choice == "2":
                self._run_tool("tools.utils.file_analyzer:FileAnalyzer")
            elif choice == "3":
                self._run_tool("tools.utils.network_scanner:NetworkScanner")
            elif choice == "4":
                self._run_tool("tools.utils.system_info:SystemInfo")
            elif choice == "5":
                break
    
    def _show_config_menu(self):
        """Zeigt Konfigurationsmenü"""
        while True:
            print("\n--- CONFIGURATION ---")
            print("1. View Current Config")
            print("2. Edit Config")
            print("3. Reset to Default")
            print("4. Validate Config")
            print("5. Back")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                print("\nCurrent Configuration:")
                import json
                print(json.dumps(self.config.config, indent=2))
            elif choice == "2":
                self._edit_config()
            elif choice == "3":
                self._reset_config()
            elif choice == "4":
                if self.config.validate():
                    print("✓ Configuration is valid")
                else:
                    print("✗ Configuration is invalid")
            elif choice == "5":
                break
    
    def _show_reports_menu(self):
        """Zeigt Reports Menü"""
        while True:
            print("\n--- REPORTS ---")
            print("1. Generate Pentest Report")
            print("2. View Recent Reports")
            print("3. Export Reports")
            print("4. Back")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self._generate_report()
            elif choice == "2":
                self._view_reports()
            elif choice == "3":
                self._export_reports()
            elif choice == "4":
                break
    
    def _run_tool(self, tool_path: str):
        """Startet ein Tool"""
        try:
            # Import dynamisch
            if ":" in tool_path:
                module_path, class_name = tool_path.split(":", 1)
            else:
                module_path, class_name = tool_path.rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            tool_class = getattr(module, class_name)
            
            # Tool instanziieren und ausführen
            tool = tool_class()
            tool.run()
            
        except ImportError as e:
            self.logger.error(f"Tool not available: {e}")
            print(f"Install required modules for {tool_path}")
        except Exception as e:
            self.logger.error(f"Tool error: {e}")
    
    def _edit_config(self):
        """Bearbeitet Konfiguration"""
        print("\nEdit Configuration (key=value, empty to finish):")
        
        while True:
            entry = input("> ").strip()
            
            if not entry:
                break
            
            if '=' in entry:
                key, value = entry.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Typ-Konvertierung versuchen
                try:
                    if value.lower() == 'true':
                        value = True
                    elif value.lower() == 'false':
                        value = False
                    elif value.isdigit():
                        value = int(value)
                    elif value.replace('.', '', 1).isdigit():
                        value = float(value)
                except:
                    pass
                
                self.config.set(key, value)
                print(f"Set {key} = {value}")
    
    def _reset_config(self):
        """Setzt Konfiguration zurück"""
        confirm = input("Are you sure you want to reset to default config? (yes/NO): ").strip().lower()
        
        if confirm == "yes":
            import shutil
            config_file = Path("blackops_config.json")
            
            if config_file.exists():
                backup = config_file.with_suffix('.json.backup')
                shutil.copy2(config_file, backup)
                config_file.unlink()
            
            self.config = ConfigManager()
            print("Configuration reset to defaults")
    
    def _generate_report(self):
        """Generiert Report"""
        print("\nGenerate Report:")
        target = input("Target: ").strip()
        report_type = input("Report Type (pentest/vuln/scan): ").strip()
        
        if not self.ethics.check_target(target):
            print("Target not authorized!")
            return
        
        print(f"Generating {report_type} report for {target}...")
        # Report generation logic here
    
    def _view_reports(self):
        """Zeigt Reports"""
        reports_dir = Path("reports")
        
        if not reports_dir.exists():
            print("No reports directory found")
            return
        
        for report_file in reports_dir.rglob("*.json"):
            print(f"- {report_file.relative_to(reports_dir)}")
    
    def _export_reports(self):
        """Exportiert Reports"""
        print("\nExport Options:")
        print("1. CSV")
        print("2. JSON")
        print("3. PDF")
        print("4. HTML")
        
        choice = input("Format: ").strip()
        
        formats = {
            '1': 'csv',
            '2': 'json',
            '3': 'pdf',
            '4': 'html'
        }
        
        if choice in formats:
            format_type = formats[choice]
            print(f"Exporting reports to {format_type.upper()}...")
            # Export logic here

def main():
    parser = argparse.ArgumentParser(description="Black Ops Framework v2.2")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--no-ethics", action="store_true", help="Disable ethics checks (DANGEROUS)")
    
    args = parser.parse_args()
    
    framework = BlackOpsFramework()
    
    if args.debug:
        framework.logger.logger.setLevel("DEBUG")
    
    if args.no_ethics:
        framework.ethics.config["approval_required"] = False
        print("WARNING: Ethics checks disabled!")
    
    try:
        framework.run()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        framework.logger.error(f"Framework error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
