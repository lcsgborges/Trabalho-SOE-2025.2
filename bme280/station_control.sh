#!/bin/bash

# Script de Controle da Estação Meteorológica BME280
# Sistema unificado para gerenciar a estação meteorológica

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
PROJECT_DIR="/home/pi/Faculdade/Trabalhos/trabalho-soe/bme280"
SERVICE_NAME="bme280-station"
LOG_FILE="/var/log/bme280-station.log"

# Função para exibir cabeçalho
show_header() {
    echo -e "${BLUE}==========================================${NC}"
    echo -e "${BLUE}    ESTAÇÃO METEOROLÓGICA BME280${NC}"
    echo -e "${BLUE}==========================================${NC}"
    echo ""
}

# Função para exibir informações da estação
show_info() {
    show_header
    
    # Obtém IP local
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    
    echo -e "${GREEN}Informações da Estação:${NC}"
    echo -e "  IP: ${YELLOW}$LOCAL_IP${NC}"
    echo -e "  URL: ${YELLOW}http://$LOCAL_IP:5000${NC}"
    echo -e "  API: ${YELLOW}http://$LOCAL_IP:5000/api/data${NC}"
    echo ""
    
    # Verifica status do serviço
    if systemctl is-active --quiet $SERVICE_NAME 2>/dev/null; then
        echo -e "${GREEN}Status: ${NC}Rodando"
        echo -e "${GREEN}Coleta: ${NC}A cada minuto"
        echo -e "${GREEN}Interface: ${NC}Atualização automática"
    else
        echo -e "${RED}Status: ${NC}Parado"
        echo -e "${YELLOW}Para iniciar: ${NC}sudo systemctl start $SERVICE_NAME"
    fi
    
    echo -e "${BLUE}==========================================${NC}"
    echo ""
}

# Função para iniciar a estação
start_station() {
    echo -e "${GREEN}Iniciando estação meteorológica...${NC}"
    
    if systemctl is-active --quiet $SERVICE_NAME 2>/dev/null; then
        echo -e "${YELLOW}Estação já está rodando${NC}"
        return 0
    fi
    
    sudo systemctl start $SERVICE_NAME
    
    if systemctl is-active --quiet $SERVICE_NAME 2>/dev/null; then
        echo -e "${GREEN}Estação iniciada com sucesso!${NC}"
        show_info
    else
        echo -e "${RED}Erro ao iniciar estação${NC}"
        echo -e "${YELLOW}Verifique os logs: ${NC}sudo journalctl -u $SERVICE_NAME -f"
        return 1
    fi
}

# Função para parar a estação
stop_station() {
    echo -e "${YELLOW}Parando estação meteorológica...${NC}"
    
    if ! systemctl is-active --quiet $SERVICE_NAME 2>/dev/null; then
        echo -e "${YELLOW}Estação já está parada${NC}"
        return 0
    fi
    
    sudo systemctl stop $SERVICE_NAME
    
    if ! systemctl is-active --quiet $SERVICE_NAME 2>/dev/null; then
        echo -e "${GREEN}Estação parada com sucesso!${NC}"
    else
        echo -e "${RED}Erro ao parar estação${NC}"
        return 1
    fi
}

# Função para reiniciar a estação
restart_station() {
    echo -e "${YELLOW}Reiniciando estação meteorológica...${NC}"
    
    sudo systemctl restart $SERVICE_NAME
    
    sleep 3
    
    if systemctl is-active --quiet $SERVICE_NAME 2>/dev/null; then
        echo -e "${GREEN}Estação reiniciada com sucesso!${NC}"
        show_info
    else
        echo -e "${RED}Erro ao reiniciar estação${NC}"
        echo -e "${YELLOW}Verifique os logs: ${NC}sudo journalctl -u $SERVICE_NAME -f"
        return 1
    fi
}

# Função para mostrar status
show_status() {
    show_header
    
    echo -e "${GREEN}Status do Serviço:${NC}"
    sudo systemctl status $SERVICE_NAME --no-pager -l
    
    echo ""
    echo -e "${GREEN}Informações de Rede:${NC}"
    show_info
}

# Função para mostrar logs
show_logs() {
    echo -e "${GREEN}Logs da Estação Meteorológica (Ctrl+C para sair):${NC}"
    echo ""
    sudo journalctl -u $SERVICE_NAME -f
}

# Função para instalar/desinstalar
install_station() {
    echo -e "${GREEN}Instalando estação meteorológica...${NC}"
    
    if [ ! -f "$PROJECT_DIR/install.py" ]; then
        echo -e "${RED}Arquivo install.py não encontrado em $PROJECT_DIR${NC}"
        return 1
    fi
    
    cd "$PROJECT_DIR"
    sudo python3 install.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Instalação concluída!${NC}"
        show_info
    else
        echo -e "${RED}Erro na instalação${NC}"
        return 1
    fi
}

uninstall_station() {
    echo -e "${YELLOW}Desinstalando estação meteorológica...${NC}"
    
    if [ ! -f "$PROJECT_DIR/install.py" ]; then
        echo -e "${RED}Arquivo install.py não encontrado em $PROJECT_DIR${NC}"
        return 1
    fi
    
    cd "$PROJECT_DIR"
    sudo python3 install.py uninstall
    
    echo -e "${GREEN}Desinstalação concluída!${NC}"
}

# Função para testar sensor
test_sensor() {
    echo -e "${GREEN}Testando sensor BME280...${NC}"
    
    if [ ! -f "$PROJECT_DIR/bme280_station.py" ]; then
        echo -e "${RED}Arquivo bme280_station.py não encontrado${NC}"
        return 1
    fi
    
    cd "$PROJECT_DIR"
    python3 -c "
import smbus2
import bme280
try:
    bus = smbus2.SMBus(1)
    address = 0x76
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    print('Sensor BME280 funcionando!')
    print(f'   Temperatura: {data.temperature:.2f}°C')
    print(f'   Pressão: {data.pressure:.2f} hPa')
    print(f'   Umidade: {data.humidity:.2f}%')
except Exception as e:
    print(f'Erro no sensor: {e}')
    exit(1)
"
}

# Função para mostrar ajuda
show_help() {
    show_header
    
    echo -e "${GREEN}Comandos disponíveis:${NC}"
    echo ""
    echo -e "  ${YELLOW}start${NC}     - Iniciar estação meteorológica"
    echo -e "  ${YELLOW}stop${NC}      - Parar estação meteorológica"
    echo -e "  ${YELLOW}restart${NC}   - Reiniciar estação meteorológica"
    echo -e "  ${YELLOW}status${NC}    - Mostrar status do serviço"
    echo -e "  ${YELLOW}logs${NC}      - Mostrar logs em tempo real"
    echo -e "  ${YELLOW}info${NC}      - Mostrar informações da estação"
    echo -e "  ${YELLOW}test${NC}      - Testar sensor BME280"
    echo -e "  ${YELLOW}install${NC}   - Instalar estação meteorológica"
    echo -e "  ${YELLOW}uninstall${NC} - Desinstalar estação meteorológica"
    echo -e "  ${YELLOW}help${NC}      - Mostrar esta ajuda"
    echo ""
    echo -e "${GREEN}Exemplos:${NC}"
    echo -e "  $0 start"
    echo -e "  $0 status"
    echo -e "  $0 logs"
    echo ""
}

# Função principal
main() {
    case "${1:-help}" in
        start)
            start_station
            ;;
        stop)
            stop_station
            ;;
        restart)
            restart_station
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        info)
            show_info
            ;;
        test)
            test_sensor
            ;;
        install)
            install_station
            ;;
        uninstall)
            uninstall_station
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}Comando inválido: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Executa função principal
main "$@"
