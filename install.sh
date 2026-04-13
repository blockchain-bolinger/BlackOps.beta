#!/bin/bash
# Black Ops Framework Installer v2.2

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${RED}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║      ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗ ███████╗║"
    echo "║      ██╔══██╗██║     ██╔══██╗██╔════╝██║  ██║██╔══██╗██╔════╝║"
    echo "║      ██████╔╝██║     ███████║██║     ███████║██████╔╝███████╗║"
    echo "║      ██╔══██╗██║     ██╔══██║██║     ██╔══██║██╔═══╝ ╚════██║║"
    echo "║      ██████╔╝███████╗██║  ██║╚██████╗██║  ██║██║     ███████║║"
    echo "║      ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝║"
    echo "║                                                              ║"
    echo "║                   FRAMEWORK v2.2 - INSTALLER                  ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

check_root() {
    if [[ $EUID -eq 0 ]]; then
        echo -e "${YELLOW}[!] Running as root${NC}"
        return 0
    else
        echo -e "${RED}[!] This script requires root privileges${NC}"
        return 1
    fi
}

check_python() {
    echo -e "${GREEN}[*] Checking Python version...${NC}"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        echo -e "${GREEN}[+] Python $PYTHON_VERSION found${NC}"
        
        # Check Python version >= 3.8
        if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
            return 0
        else
            echo -e "${RED}[!] Python 3.8 or higher required${NC}"
            return 1
        fi
    else
        echo -e "${RED}[!] Python3 not found${NC}"
        return 1
    fi
}

install_dependencies() {
    echo -e "${GREEN}[*] Installing system dependencies...${NC}"
    
    # Detect OS
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        apt-get update
        apt-get install -y \
            python3-pip \
            python3-venv \
            git \
            nmap \
            wireshark \
            tcpdump \
            net-tools \
            libpcap-dev \
            libssl-dev \
            libffi-dev \
            build-essential
        
    elif [ -f /etc/redhat-release ]; then
        # RHEL/CentOS/Fedora
        yum install -y \
            python3-pip \
            python3-devel \
            git \
            nmap \
            wireshark \
            tcpdump \
            net-tools \
            libpcap-devel \
            openssl-devel \
            libffi-devel \
            gcc
        
    elif [ -f /etc/arch-release ]; then
        # Arch Linux
        pacman -Syu --noconfirm \
            python-pip \
            python-virtualenv \
            git \
            nmap \
            wireshark-qt \
            tcpdump \
            net-tools \
            libpcap \
            openssl \
            libffi \
            base-devel
        
    else
        echo -e "${YELLOW}[!] Unsupported OS. Manual dependency installation required.${NC}"
    fi
}

setup_venv() {
    echo -e "${GREEN}[*] Setting up Python virtual environment...${NC}"
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
}

install_python_packages() {
    echo -e "${GREEN}[*] Installing Python packages...${NC}"
    
    # Install from requirements.txt
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo -e "${YELLOW}[!] requirements.txt not found${NC}"
    fi
    
    # Additional packages
    pip install \
        ipython \
        jupyter \
        pylint \
        autopep8
}

setup_directories() {
    echo -e "${GREEN}[*] Setting up directory structure...${NC}"
    
    # Create required directories
    mkdir -p \
        logs/audit \
        logs/framework \
        logs/tools \
        data/wordlists \
        data/configs \
        data/templates \
        reports/pentest \
        reports/exports \
        payloads \
        backups \
        tmp
    
    # Set permissions
    chmod 700 logs
    chmod 600 data/configs/*.json 2>/dev/null || true
}

download_wordlists() {
    echo -e "${GREEN}[*] Downloading wordlists...${NC}"
    
    WORDLIST_DIR="data/wordlists"
    
    # Common passwords
    if [ ! -f "$WORDLIST_DIR/common_passwords.txt" ]; then
        echo -e "${GREEN}[+] Downloading common passwords...${NC}"
        curl -s -o "$WORDLIST_DIR/common_passwords.txt" \
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"
    fi
    
    # Usernames
    if [ ! -f "$WORDLIST_DIR/usernames.txt" ]; then
        echo -e "${GREEN}[+] Downloading usernames...${NC}"
        curl -s -o "$WORDLIST_DIR/usernames.txt" \
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/Names/names.txt"
    fi
    
    # Subdomains
    if [ ! -f "$WORDLIST_DIR/subdomains.txt" ]; then
        echo -e "${GREEN}[+] Downloading subdomains...${NC}"
        curl -s -o "$WORDLIST_DIR/subdomains.txt" \
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt"
    fi
}

setup_config() {
    echo -e "${GREEN}[*] Setting up configuration...${NC}"
    
    # Create default config if not exists
    if [ ! -f "blackops_config.json" ]; then
        cat > blackops_config.json << EOF
{
  "version": "2.2.0",
  "debug": false,
  "log_level": "INFO",
  "encryption": {
    "algorithm": "AES-256-GCM",
    "key_rotation_days": 30
  },
  "network": {
    "timeout": 30,
    "max_retries": 3,
    "proxy": null
  },
  "ethics": {
    "allowed_targets": [],
    "forbidden_actions": [
      "data_destruction",
      "ransomware",
      "service_disruption"
    ],
    "require_approval": true
  }
}
EOF
    fi
    
    # Create secrets template
    if [ ! -f "secrets.json" ]; then
        cat > secrets.json << EOF
{
  "api_keys": {
    "shodan": "YOUR_SHODAN_API_KEY",
    "virustotal": "YOUR_VIRUSTOTAL_API_KEY",
    "haveibeenpwned": "YOUR_HIBP_API_KEY"
  },
  "credentials": {
    "username": "",
    "password": ""
  },
  "encryption": {
    "master_key": ""
  }
}
EOF
        chmod 600 secrets.json
    fi
}

setup_geolite() {
    echo -e "${GREEN}[*] Setting up GeoLite2 database...${NC}"
    
    GEOIP_DIR="data/geoip"
    mkdir -p "$GEOIP_DIR"
    
    # Check if files already exist
    if [ ! -f "$GEOIP_DIR/GeoLite2-City.mmdb" ] || [ ! -f "$GEOIP_DIR/GeoLite2-Country.mmdb" ]; then
        echo -e "${YELLOW}[!] GeoLite2 databases not found${NC}"
        echo -e "${YELLOW}[!] Download from: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data${NC}"
        echo -e "${YELLOW}[!] Place .mmdb files in $GEOIP_DIR${NC}"
    fi
}

post_install() {
    echo -e "${GREEN}[*] Running post-installation tasks...${NC}"
    
    # Make scripts executable
    chmod +x black_ops.py
    chmod +x run.sh
    
    # Create run.sh script
    cat > run.sh << 'EOF'
#!/bin/bash
# Black Ops Framework Runner

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Virtual environment not found. Run install.sh first."
    exit 1
fi

# Run framework
cd "$SCRIPT_DIR"
python3 black_ops.py "$@"
EOF
    
    chmod +x run.sh
    
    # Create uninstall script
    cat > uninstall.sh << 'EOF'
#!/bin/bash
# Black Ops Framework Uninstaller

set -e

read -p "Are you sure you want to uninstall Black Ops Framework? (yes/NO): " confirm

if [ "$confirm" = "yes" ]; then
    echo "Removing virtual environment..."
    rm -rf venv
    
    echo "Removing logs and temporary files..."
    rm -rf logs/* tmp/* backups/*
    
    echo "Keeping configuration and data files..."
    
    echo "Uninstallation complete."
    echo "Note: Configuration files and reports were kept."
else
    echo "Uninstallation cancelled."
fi
EOF
    
    chmod +x uninstall.sh
}

show_completion() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    INSTALLATION COMPLETE                     ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                                                              ║"
    echo "║  Next Steps:                                                 ║"
    echo "║  1. Edit secrets.json with your API keys                    ║"
    echo "║  2. Review blackops_config.json                             ║"
    echo "║  3. Run: ./run.sh                                           ║"
    echo "║                                                              ║"
    echo "║  Quick Start:                                               ║"
    echo "║    ./run.sh --help                                          ║"
    echo "║    ./run.sh                                                 ║"
    echo "║                                                              ║"
    echo "║  Remember:                                                  ║"
    echo "║  - Use only for authorized testing                          ║"
    echo "║  - Respect all laws and regulations                         ║"
    echo "║  - Obtain proper permissions                                ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

main() {
    print_banner
    
    echo -e "${YELLOW}[!] This installer requires root privileges${NC}"
    echo -e "${YELLOW}[!] Use only for authorized security testing${NC}"
    echo ""
    
    # Check requirements
    check_root || exit 1
    check_python || exit 1
    
    # Installation steps
    install_dependencies
    setup_venv
    install_python_packages
    setup_directories
    download_wordlists
    setup_config
    setup_geolite
    post_install
    
    show_completion
}

# Run main function
main "$@"