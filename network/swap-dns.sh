#!/bin/bash

# Check for required argument
NEW_DNS="$1"
CONN_NAME="$2"

if [ -z "$NEW_DNS" ]; then
    echo "Usage: $0 <new_dns_ip> [connection_name]"
    exit 1
fi

# Detect active connection name if not provided
if [ -z "$CONN_NAME" ]; then
    CONN_NAME=$(nmcli -t -f NAME connection show --active | head -n1)
fi

echo "[*] Using connection: $CONN_NAME"

# Get current DNS servers
CURRENT_DNS_LIST=($(nmcli dev show | grep IP4.DNS | awk '{print $2}'))
CURRENT_PRIMARY_DNS="${CURRENT_DNS_LIST[0]}"

echo "[*] Current DNS detected: ${CURRENT_DNS_LIST[*]}"
echo "[*] New primary DNS requested: $NEW_DNS"

# Check if the new DNS is already the primary one
if [ "$NEW_DNS" == "$CURRENT_PRIMARY_DNS" ]; then
    echo "[*] New DNS is already set as primary. No changes needed."
    exit 0
fi

# Disable automatic DNS from DHCP
nmcli connection modify "$CONN_NAME" ipv4.ignore-auto-dns yes

# Set new DNS + existing primary as secondary
nmcli connection modify "$CONN_NAME" ipv4.dns "$NEW_DNS $CURRENT_PRIMARY_DNS"

# Restart the connection
echo "[*] Applying changes..."
nmcli connection down "$CONN_NAME" && nmcli connection up "$CONN_NAME"

# Confirm changes
echo "[*] DNS updated successfully:"
nmcli dev show | grep IP4.DNS