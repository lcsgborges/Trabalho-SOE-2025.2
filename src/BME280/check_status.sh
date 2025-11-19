#!/bin/bash

# Script para verificar status do servidor BME280

echo "=== Status do Servidor BME280 ==="
echo ""

# Verificar se o processo está rodando
if pgrep -x "bme280_server" > /dev/null; then
    echo "Servidor está RODANDO"
    
    # Pegar o PID
    PID=$(pgrep -x "bme280_server")
    echo "   PID: $PID"
    
    # Verificar há quanto tempo está rodando
    echo "   Tempo ativo: $(ps -o etime= -p $PID)"
    
    # Obter IP
    IP=$(hostname -I | awk '{print $1}')
    
    echo ""
    echo "┌─────────────────────────────────────────┐"
    echo "│  Acesse o Dashboard:                    │"
    echo "│                                         │"
    echo "│  http://$IP:8080                        │"
    echo "│                                         │"
    echo "└─────────────────────────────────────────┘"
    echo ""
    
    # Verificar porta
    if netstat -tuln 2>/dev/null | grep -q ":8080"; then
        echo "Porta 8080 está aberta"
    else
        echo "Porta 8080 pode não estar acessível"
    fi
    
else
    echo "Servidor NÃO está rodando"
    echo ""
    echo "Para iniciar:"
    echo "  ./start_server.sh"
    echo ""
    echo "Ou verifique o serviço systemd:"
    echo "  sudo systemctl status bme280"
    echo ""
fi

# Verificar se o serviço systemd está ativo
echo ""
echo "--- Status do Serviço Systemd ---"
if systemctl is-enabled bme280.service &>/dev/null; then
    echo "Auto-inicialização: ATIVADA"
else
    echo "Auto-inicialização: DESATIVADA"
fi

if systemctl is-active bme280.service &>/dev/null; then
    echo "Serviço systemd: ATIVO"
else
    echo "Serviço systemd: INATIVO"
fi

echo ""
echo "Comandos úteis:"
echo "  Ver logs completos: tail -f /tmp/bme280.log"
echo "  Parar servidor: sudo pkill bme280_server"
echo "  Status systemd: sudo systemctl status bme280"
