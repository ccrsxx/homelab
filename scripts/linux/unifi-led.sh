#!/bin/bash
# Unified UniFi LED controller
# Usage: unifi_led.sh <on|off>

# ==== Configuration ====
SSH_KEY="/home/ccrsxx/.ssh/homelab-automation.key"
SSH_USER="ccrsxx"

# List of AP IPs
APS=(
  "192.168.20.100"
  "192.168.20.110"
)

# Path to config file on each AP
CFG="/var/etc/persistent/cfg/mgmt"
# =======================

STATE="$1"

if [[ -z "$STATE" ]]; then
  echo "Usage: $0 <on|off>"
  exit 1
fi

if [[ "$STATE" != "on" && "$STATE" != "off" ]]; then
  echo "Invalid state: $STATE (must be 'on' or 'off')"
  exit 1
fi

# Define replacements based on desired state
if [[ "$STATE" == "on" ]]; then
  FROM="mgmt.led_enabled=false"
  TO="mgmt.led_enabled=true"
  MSG="Turning LED ON"
else
  FROM="mgmt.led_enabled=true"
  TO="mgmt.led_enabled=false"
  MSG="Turning LED OFF"
fi

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

echo "[$(timestamp)] $MSG"

for AP_IP in "${APS[@]}"; do
  echo "[$(timestamp)] AP $AP_IP"
  ssh -i "$SSH_KEY" -o ConnectTimeout=5 -o StrictHostKeyChecking=no "${SSH_USER}@${AP_IP}" sh -s <<EOF
if [ -f "$CFG" ]; then
  if grep -q "$FROM" "$CFG"; then
    sed -i "s/$FROM/$TO/" "$CFG"
    echo "[$(timestamp)] LED state changed to $STATE"
  else
    echo "[$(timestamp)] LED already $STATE"
  fi
  syswrapper.sh save-config
else
  echo "Error: config file not found ($CFG)"
fi
EOF
done

echo "[$(timestamp)] Completed LED $STATE action"
