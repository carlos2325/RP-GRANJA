#!/bin/sh

set -e

IP="${1:-192.168.1.135}"
CONFIG="$HOME/.ssh/config"
SSH_DIR="$HOME/.ssh"

mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"
touch "$CONFIG"
chmod 600 "$CONFIG"

if grep -q "Host granja" "$CONFIG" 2>/dev/null; then
  echo "Ya existe el host 'granja' en $CONFIG"
  exit 0
fi

echo "" >> "$CONFIG"
echo "Host granja" >> "$CONFIG"
echo "    HostName $IP" >> "$CONFIG"
echo "    User pi" >> "$CONFIG"
echo "    IdentityFile $HOME/.ssh/granja_iot" >> "$CONFIG"
echo "    IdentitiesOnly yes" >> "$CONFIG"
echo "    AddKeysToAgent yes" >> "$CONFIG"

echo "Listo. Se ha añadido el host 'granja' a $CONFIG (IP: $IP)"
echo "Prueba: ssh granja"
