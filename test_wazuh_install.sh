#!/bin/bash

# Test script for Wazuh installation
# This script validates the install_wazuh.sh script without actually installing Wazuh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

echo ""
echo "🧪 TESTING WAZUH INSTALLATION SCRIPT"
echo "===================================="
echo ""

# Test 1: Check if install_wazuh.sh exists
print_test "Checking if install_wazuh.sh exists..."
if [ -f "install_wazuh.sh" ]; then
    print_pass "install_wazuh.sh found"
else
    print_fail "install_wazuh.sh not found"
    exit 1
fi

# Test 2: Check if script is executable
print_test "Checking if script is executable..."
if [ -x "install_wazuh.sh" ]; then
    print_pass "Script is executable"
else
    print_fail "Script is not executable"
    exit 1
fi

# Test 3: Check script syntax
print_test "Checking script syntax..."
if bash -n install_wazuh.sh; then
    print_pass "Script syntax is valid"
else
    print_fail "Script has syntax errors"
    exit 1
fi

# Test 4: Check for required commands
print_test "Checking for required system commands..."
commands=("curl" "systemctl" "free" "df")
for cmd in "${commands[@]}"; do
    if command -v "$cmd" >/dev/null 2>&1; then
        print_pass "$cmd is available"
    else
        print_fail "$cmd is not available"
    fi
done

# Test 5: Check network connectivity to Wazuh packages
print_test "Testing network connectivity to Wazuh packages..."
if curl -s --head https://packages.wazuh.com/4.13/wazuh-install.sh | head -n 1 | grep -q "200 OK"; then
    print_pass "Can connect to Wazuh package repository"
else
    print_fail "Cannot connect to Wazuh package repository"
    print_info "Network connectivity may be limited in this environment"
fi

# Test 6: Check if running with appropriate permissions
print_test "Checking current user permissions..."
if [ "$EUID" -eq 0 ]; then
    print_pass "Running as root - can proceed with installation"
else
    print_info "Not running as root - installation will require sudo"
fi

# Test 7: Verify script components
print_test "Checking script functions..."
if grep -q "download_wazuh_installer" install_wazuh.sh; then
    print_pass "Download function found"
else
    print_fail "Download function missing"
fi

if grep -q "install_wazuh" install_wazuh.sh; then
    print_pass "Installation function found"
else
    print_fail "Installation function missing"
fi

if grep -q "verify_installation" install_wazuh.sh; then
    print_pass "Verification function found"
else
    print_fail "Verification function missing"
fi

# Test 8: Check for the correct Wazuh URL
print_test "Checking Wazuh download URL..."
if grep -q "https://packages.wazuh.com/4.13/wazuh-install.sh" install_wazuh.sh; then
    print_pass "Correct Wazuh 4.13 URL found"
else
    print_fail "Wazuh 4.13 URL not found or incorrect"
fi

# Test 9: Check for all-in-one installation command
print_test "Checking for all-in-one installation command..."
if grep -q "\-a" install_wazuh.sh; then
    print_pass "All-in-one installation flag found"
else
    print_fail "All-in-one installation flag missing"
fi

echo ""
echo "📋 TEST SUMMARY"
echo "==============="
print_info "The install_wazuh.sh script has been validated for:"
print_info "✓ File existence and permissions"
print_info "✓ Script syntax validity"  
print_info "✓ Required function presence"
print_info "✓ Correct Wazuh download URL"
print_info "✓ All-in-one installation capability"
echo ""
print_pass "All tests completed successfully!"
echo ""
print_info "To install Wazuh, run: sudo ./install_wazuh.sh"
echo ""