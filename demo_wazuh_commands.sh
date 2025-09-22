#!/bin/bash

# Demo script showing Wazuh installation commands for CRPF Log Analyzer
# This demonstrates the exact commands that would be executed

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_demo() {
    echo -e "${CYAN}[DEMO]${NC} $1"
}

print_command() {
    echo -e "${YELLOW}\$${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

echo ""
echo "🛡️  CRPF LOG ANALYZER - WAZUH INSTALLATION DEMO"
echo "==============================================="
echo ""

print_info "This demo shows the exact commands used to download and install Wazuh"
print_info "in all-in-one mode for the CRPF Log Analyzer system."
echo ""

print_demo "Step 1: Download Wazuh installation script"
print_command "curl -sO https://packages.wazuh.com/4.13/wazuh-install.sh"
echo ""
print_info "This downloads the official Wazuh 4.13 installation script"
print_info "The -s flag makes curl silent, -O saves with the original filename"
echo ""

print_demo "Step 2: Make the script executable"
print_command "chmod +x wazuh-install.sh"
echo ""

print_demo "Step 3: Run Wazuh installation in all-in-one mode"
print_command "sudo bash ./wazuh-install.sh -a"
echo ""
print_info "The -a flag installs all Wazuh components on a single server:"
print_info "• Wazuh Manager: Central management and analysis engine"
print_info "• Wazuh Indexer: Data storage and indexing (OpenSearch-based)"
print_info "• Wazuh Dashboard: Web interface for monitoring and management"
print_info "• Filebeat: Log shipping and data collection"
echo ""

print_demo "Alternative: Use the CRPF integration script"
print_command "sudo ./install_wazuh.sh"
echo ""
print_info "Our custom integration script includes:"
print_info "• System requirements checking"
print_info "• Configuration backup"
print_info "• Enhanced logging and error handling"
print_info "• Post-installation verification"
print_info "• CRPF-specific integration guidance"
echo ""

print_demo "Post-installation verification"
print_command "systemctl status wazuh-manager"
print_command "systemctl status wazuh-indexer"
print_command "systemctl status wazuh-dashboard"
print_command "systemctl status filebeat"
echo ""

print_demo "Access Wazuh Dashboard"
print_info "URL: https://localhost:443 or https://YOUR_SERVER_IP:443"
print_info "Default credentials: admin / admin"
print_info "⚠️  Change the default password immediately after first login"
echo ""

print_demo "Integration with CRPF Log Analyzer"
print_info "Once both systems are running:"
print_info "1. Configure Wazuh to receive logs from CRPF infrastructure"
print_info "2. Set up log forwarding from existing services to Wazuh"
print_info "3. Create custom rules for CRPF-specific security events"
print_info "4. Configure alerting for critical security incidents"
echo ""

print_demo "Network Configuration"
print_info "Ensure these ports are accessible:"
print_info "• 443: Wazuh Dashboard (HTTPS)"
print_info "• 1514-1516: Wazuh Agent communication"
print_info "• 9200: Wazuh Indexer API"
print_info "• 55000: Wazuh Manager API"
echo ""

echo "🎯 DEPLOYMENT STRATEGY FOR CRPF"
echo "==============================="
print_info "1. Install Wazuh on central monitoring server"
print_info "2. Deploy Wazuh agents to all CRPF location servers"
print_info "3. Configure log collection from existing CRPF systems"
print_info "4. Set up dashboards for different CRPF units"
print_info "5. Implement alerting for security incidents"
print_info "6. Train CRPF security analysts on the system"
echo ""

echo "✅ Ready to deploy Wazuh for CRPF centralized security monitoring!"
echo ""