#!/bin/bash

# Script de instalação e configuração automática para Raspberry Pi

echo "╔═══════════════════════════════════════════════╗"
echo "║  Instalação Automática - Servidor BME280      ║"
echo "║  Raspberry Pi 3 Model B                       ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Verificar se está rodando na Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "Aviso: Pode não estar rodando em uma Raspberry Pi"
fi

# 1. Atualizar e instalar dependências
echo "[1/7] Instalando dependências..."
sudo apt-get update -qq
sudo apt-get install -y git build-essential g++ i2c-tools net-tools > /dev/null 2>&1

# 2. Instalar WiringPi
echo "[2/7] Instalando WiringPi..."
if [ ! -d "/tmp/WiringPi" ]; then
    cd /tmp
    git clone https://github.com/WiringPi/WiringPi.git > /dev/null 2>&1
    cd WiringPi
    sudo ./build > /dev/null 2>&1
fi

# 3. Habilitar I2C
echo "[3/7] Habilitando I2C..."
sudo raspi-config nonint do_i2c 0
sudo usermod -a -G i2c pi

# 4. Criar diretórios
echo "[4/7] Criando diretórios..."
mkdir -p /home/pi/trabalho/src/database

# 5. Compilar
echo "[5/7] Compilando servidor..."
cd /home/pi/trabalho/src/BME280
make clean > /dev/null 2>&1
make > /dev/null 2>&1

if [ ! -f "./bme280_server" ]; then
    echo "Erro na compilação!"
    exit 1
fi

# 6. Configurar serviço systemd
echo "[6/7] Configurando inicialização automática..."
sudo cp bme280.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bme280.service

# 7. Tornar scripts executáveis
echo "[7/7] Configurando scripts..."
chmod +x start_server.sh check_status.sh

echo ""
echo "Instalação concluída com sucesso!"
echo ""
echo "═══════════════════════════════════════════════════"
echo "  PRÓXIMOS PASSOS:"
echo "═══════════════════════════════════════════════════"
echo ""
echo "OPÇÃO 1 - Iniciar automaticamente no boot:"
echo "  sudo reboot"
echo ""
echo "OPÇÃO 2 - Iniciar agora manualmente:"
echo "  ./start_server.sh"
echo ""
echo "Para verificar se está rodando:"
echo "  ./check_status.sh"
echo ""
echo "═══════════════════════════════════════════════════"
