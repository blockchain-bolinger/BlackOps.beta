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
