#!/bin/bash

# Script de instalação e configuração automática para Raspberry Pi

echo "╔═══════════════════════════════════════════════╗"
echo "║  Instalação Automática - Servidor BME280     ║"
echo "║  Raspberry Pi 3 Model B                      ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Verificar se está rodando na Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "⚠️  Aviso: Pode não estar rodando em uma Raspberry Pi"
fi

# 1. Atualizar e instalar dependências
echo "[1/6] Instalando dependências..."
sudo apt-get update -qq
sudo apt-get install -y git build-essential g++ i2c-tools > /dev/null 2>&1

# 2. Instalar WiringPi
echo "[2/6] Instalando WiringPi..."
if [ ! -d "/tmp/WiringPi" ]; then
    cd /tmp
    git clone https://github.com/WiringPi/WiringPi.git > /dev/null 2>&1
    cd WiringPi
    sudo ./build > /dev/null 2>&1
fi

# 3. Habilitar I2C
echo "[3/6] Habilitando I2C..."
sudo raspi-config nonint do_i2c 0
sudo usermod -a -G i2c pi

# 4. Criar diretórios
echo "[4/6] Criando diretórios..."
mkdir -p /home/pi/trabalho/src/database

# 5. Compilar
echo "[5/6] Compilando servidor..."
cd /home/pi/trabalho/src/BME280
make clean > /dev/null 2>&1
make > /dev/null 2>&1

# 6. Configurar serviço systemd
echo "[6/6] Configurando inicialização automática..."
sudo cp bme280.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bme280.service

echo ""
echo "✅ Instalação concluída com sucesso!"
echo ""
echo "═══════════════════════════════════════════"
echo "  PRÓXIMOS PASSOS:"
echo "═══════════════════════════════════════════"
echo ""
echo "1. Reinicie a Raspberry Pi:"
echo "   sudo reboot"
echo ""
echo "2. Após reiniciar, o servidor iniciará"
echo "   automaticamente!"
echo ""
echo "3. Para ver o endereço de acesso:"
echo "   sudo systemctl status bme280"
echo ""
echo "   OU execute:"
echo "   ./start_server.sh"
echo ""
echo "═══════════════════════════════════════════"
