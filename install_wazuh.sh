#!/bin/bash

# CRPF Log Analyzer - Wazuh Integration Script
# This script downloads and installs Wazuh in all-in-one mode for CRPF security monitoring

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This script must be run as root or with sudo"
        print_status "Please run: sudo $0"
        exit 1
    fi
}

# Function to check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check if curl is installed
    if ! command -v curl &> /dev/null; then
        print_error "curl is not installed. Please install curl first."
        exit 1
    fi
    
    # Check minimum RAM (4GB recommended)
    total_ram=$(free -m | awk 'NR==2{printf "%.0f", $2}')
    if [ "$total_ram" -lt 4096 ]; then
        print_warning "System has less than 4GB RAM ($total_ram MB). Wazuh may not perform optimally."
    fi
    
    # Check available disk space (10GB minimum)
    available_space=$(df / | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 10485760 ]; then
        print_warning "Less than 10GB disk space available. Ensure sufficient space for Wazuh installation."
    fi
    
    print_success "System requirements check completed"
}

# Function to download Wazuh installation script
download_wazuh_installer() {
    print_status "Downloading Wazuh installation script..."
    
    # Remove existing installer if present
    if [ -f "wazuh-install.sh" ]; then
        print_status "Removing existing Wazuh installer..."
        rm -f wazuh-install.sh
    fi
    
    # Download the official Wazuh installer
    if curl -sO https://packages.wazuh.com/4.13/wazuh-install.sh; then
        print_success "Wazuh installation script downloaded successfully"
        chmod +x wazuh-install.sh
    else
        print_error "Failed to download Wazuh installation script"
        exit 1
    fi
}

# Function to backup existing configuration
backup_config() {
    print_status "Creating backup of existing configuration..."
    
    backup_dir="wazuh_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup existing Wazuh configuration if it exists
    if [ -d "/var/ossec" ]; then
        print_status "Backing up existing Wazuh manager configuration..."
        cp -r /var/ossec/etc "$backup_dir/wazuh-manager-etc" 2>/dev/null || true
    fi
    
    if [ -d "/etc/wazuh-indexer" ]; then
        print_status "Backing up existing Wazuh indexer configuration..."
        cp -r /etc/wazuh-indexer "$backup_dir/wazuh-indexer-etc" 2>/dev/null || true
    fi
    
    if [ -d "/etc/wazuh-dashboard" ]; then
        print_status "Backing up existing Wazuh dashboard configuration..."
        cp -r /etc/wazuh-dashboard "$backup_dir/wazuh-dashboard-etc" 2>/dev/null || true
    fi
    
    print_success "Configuration backup created in $backup_dir"
}

# Function to install Wazuh in all-in-one mode
install_wazuh() {
    print_status "Starting Wazuh installation in all-in-one mode..."
    print_warning "This may take several minutes. Please do not interrupt the process."
    
    # Run the Wazuh installer in all-in-one mode
    if bash ./wazuh-install.sh -a; then
        print_success "Wazuh installation completed successfully!"
    else
        print_error "Wazuh installation failed"
        print_status "Check the logs at /var/log/wazuh-install.log for details"
        exit 1
    fi
}

# Function to verify installation
verify_installation() {
    print_status "Verifying Wazuh installation..."
    
    # Check if Wazuh manager is running
    if systemctl is-active --quiet wazuh-manager; then
        print_success "Wazuh Manager is running"
    else
        print_warning "Wazuh Manager is not running"
    fi
    
    # Check if Wazuh indexer is running
    if systemctl is-active --quiet wazuh-indexer; then
        print_success "Wazuh Indexer is running"
    else
        print_warning "Wazuh Indexer is not running"
    fi
    
    # Check if Wazuh dashboard is running
    if systemctl is-active --quiet wazuh-dashboard; then
        print_success "Wazuh Dashboard is running"
    else
        print_warning "Wazuh Dashboard is not running"
    fi
    
    # Check if Filebeat is running
    if systemctl is-active --quiet filebeat; then
        print_success "Filebeat is running"
    else
        print_warning "Filebeat is not running"
    fi
}

# Function to display access information
display_access_info() {
    print_success "Wazuh installation completed!"
    echo ""
    echo "🛡️  WAZUH ACCESS INFORMATION"
    echo "================================"
    echo ""
    echo "🌐 Wazuh Dashboard URL: https://$(hostname -I | awk '{print $1}'):443"
    echo "🌐 Alternative access:  https://localhost:443"
    echo ""
    echo "📋 Default Credentials:"
    echo "   Username: admin"
    echo "   Password: admin"
    echo ""
    echo "⚠️  IMPORTANT SECURITY NOTES:"
    echo "   1. Change the default password immediately after first login"
    echo "   2. Configure SSL certificates for production use"
    echo "   3. Review firewall settings and open necessary ports"
    echo "   4. Check /var/log/wazuh-install.log for detailed installation logs"
    echo ""
    echo "🔧 Service Management:"
    echo "   sudo systemctl status wazuh-manager"
    echo "   sudo systemctl status wazuh-indexer" 
    echo "   sudo systemctl status wazuh-dashboard"
    echo "   sudo systemctl status filebeat"
    echo ""
    print_status "Integration with CRPF Log Analyzer:"
    print_status "Configure Wazuh to receive logs from your CRPF infrastructure"
    print_status "Update firewall rules to allow communication between systems"
}

# Main execution
main() {
    echo ""
    echo "🛡️  CRPF LOG ANALYZER - WAZUH INTEGRATION"
    echo "========================================="
    echo ""
    print_status "Starting Wazuh all-in-one installation for CRPF security monitoring"
    echo ""
    
    check_root
    check_requirements
    backup_config
    download_wazuh_installer
    install_wazuh
    verify_installation
    display_access_info
    
    echo ""
    print_success "Wazuh installation and integration setup completed successfully!"
    echo ""
}

# Run main function
main "$@"