#!/bin/bash

# Script para parar e limpar o servidor BME280

echo "=== Parando Servidor BME280 ==="
echo ""

# 1. Parar o processo
echo "[1] Parando processo bme280_server..."
if pgrep -x "bme280_server" > /dev/null; then
    sudo pkill bme280_server
    sleep 2
    if pgrep -x "bme280_server" > /dev/null; then
        echo "Processo ainda rodando, forçando..."
        sudo pkill -9 bme280_server
    fi
    echo "Processo parado"
else
    echo "ℹProcesso não estava rodando"
fi

# 2. Parar e desabilitar serviço systemd
echo ""
echo "[2] Parando serviço systemd..."
if systemctl is-active bme280.service &>/dev/null; then
    sudo systemctl stop bme280.service
    echo "Serviço parado"
else
    echo "Serviço não estava ativo"
fi

if systemctl is-enabled bme280.service &>/dev/null; then
    sudo systemctl disable bme280.service
    echo "Auto-inicialização desabilitada"
else
    echo "ℹAuto-inicialização já estava desabilitada"
fi

# 3. Remover serviço do systemd (opcional)
echo ""
echo "[3] Removendo configuração do systemd..."
if [ -f /etc/systemd/system/bme280.service ]; then
    sudo rm /etc/systemd/system/bme280.service
    sudo systemctl daemon-reload
    echo "Configuração removida"
else
    echo "ℹConfiguração não encontrada"
fi

# 4. Limpar executável (opcional)
echo ""
echo "[4] Limpando executável..."
if [ -f "./bme280_server" ]; then
    rm -f ./bme280_server
    echo "Executável removido"
else
    echo "Executável não encontrado"
fi

echo ""
echo "Limpeza concluída!"
echo ""
echo "Para reinstalar:"
echo "  ./setup_rpi.sh"
echo ""
