#!/bin/bash

# Script para iniciar o servidor BME280 em background

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Servidor BME280 ==="

# Compilar se necessário
if [ ! -f "./bme280_server" ]; then
    echo "Compilando..."
    make > /dev/null 2>&1
fi

# Criar diretório de database
mkdir -p ../database

# Verificar I2C
if ! ls /dev/i2c-* 1> /dev/null 2>&1; then
    echo "I2C não detectado. Execute: sudo raspi-config -> Interface Options -> I2C"
    exit 1
fi

# Iniciar em background
echo "Iniciando servidor em background..."
sudo nohup ./bme280_server > /tmp/bme280.log 2>&1 &

sleep 2

# Obter IP
IP=$(hostname -I | awk '{print $1}')

echo ""
echo "Servidor rodando em background!"
echo ""
echo "┌─────────────────────────────────────────┐"
echo "│  Acesse o Dashboard:                    │"
echo "│                                         │"
echo "│  http://$IP:8080                        │"
echo "│                                         │"
echo "└─────────────────────────────────────────┘"
echo ""
echo "Comandos úteis:"
echo "  Ver logs: tail -f /tmp/bme280.log"
echo "  Parar: sudo pkill bme280_server"
echo ""
