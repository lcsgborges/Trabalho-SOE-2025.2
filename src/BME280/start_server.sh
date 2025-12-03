#!/bin/bash

# Script para iniciar o servidor BME280 e servidor de predições em background

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Caminho do servidor de predições
PREDICTION_SERVER="$SCRIPT_DIR/../../model/python/prediction_server.py"

echo "=== Servidor BME280 + Predições IA ==="

# Compilar se necessário
if [ ! -f "./bme280_server" ]; then
    echo "Compilando servidor BME280..."
    make > /dev/null 2>&1
fi

# Criar diretório de database
mkdir -p ../database

# Verificar I2C
if ! ls /dev/i2c-* 1> /dev/null 2>&1; then
    echo "I2C não detectado. Execute: sudo raspi-config -> Interface Options -> I2C"
    exit 1
fi

# Iniciar servidor BME280 em background
echo "Iniciando servidor BME280 em background..."
sudo nohup ./bme280_server > /tmp/bme280.log 2>&1 &
BME280_PID=$!

sleep 2

# Verificar se Python está disponível
if command -v python3 &> /dev/null; then
    # Verificar se o script de predição existe
    if [ -f "$PREDICTION_SERVER" ]; then
        echo "Iniciando servidor de predições (IA) em background..."
	cd /home/pi/trabalho/model; source venv/bin/activate 
        nohup python3 "$PREDICTION_SERVER" > /tmp/prediction_server.log 2>&1 &
        PREDICTION_PID=$!
        sleep 2
        
        if ps -p $PREDICTION_PID > /dev/null 2>&1; then
            echo "Servidor de predições iniciado (PID: $PREDICTION_PID)"
        else
            echo "[AVISO] Servidor de predições falhou ao iniciar"
            echo "        Verifique: tail -f /tmp/prediction_server.log"
        fi
    else
        echo "[AVISO] Servidor de predições não encontrado: $PREDICTION_SERVER"
    fi
else
    echo "[AVISO] Python3 não encontrado - servidor de predições não iniciado"
fi

# Obter IP
IP=$(hostname -I | awk '{print $1}')

echo ""
echo "Servidores rodando em background!"
echo ""
echo "┌─────────────────────────────────────────┐"
echo "│  Dashboard:  http://$IP:8080            │"
echo "│  API Sensor: http://$IP:8080/api/data   │"
echo "│  API IA:     http://$IP:5000/api/predict│"
echo "└─────────────────────────────────────────┘"
echo ""
echo "Comandos úteis:"
echo "  Logs BME280:    tail -f /tmp/bme280.log"
echo "  Logs Predição:  tail -f /tmp/prediction_server.log"
echo "  Parar tudo:     ./stop_and_clean.sh"
echo ""
