#!/usr/bin/env python3
"""
Script para instalação e configuração do sistema.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class BME280Installer:
    """Instalador da estação meteorológica BME280"""

    def __init__(self):
        self.project_dir = Path(__file__).parent.absolute()
        self.service_file = "/etc/systemd/system/bme280-station.service"
        self.log_file = "/var/log/bme280-station.log"
        self.pid_file = "/var/run/bme280-station.pid"
        
    def print_header(self):
        """Exibe cabeçalho do instalador"""
        print("\n" + "="*60)
        print("    INSTALADOR ESTAÇÃO METEOROLÓGICA BME280")
        print("="*60)
        print()
    
    def check_root(self):
        """Verifica se está rodando como root"""
        if os.geteuid() != 0:
            print("   Este script deve ser executado como root (use sudo)")
            print("   sudo python3 install.py")
            return False
        return True
    
    def check_dependencies(self):
        """Verifica e instala dependências"""
        print("    Verificando dependências...")
        
        # Instala dependências Python
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", "requirements.txt"
            ], check=True, cwd=self.project_dir)
            print("Dependências Python instaladas")
        except subprocess.CalledProcessError:
            print("Erro ao instalar dependências Python")
            return False
        
        return True

    def check_sensor(self):
        """Verifica se o sensor está conectado"""
        print("Verificando sensor BME280...")
        
        try:
            # Testa importação e conexão com sensor
            result = subprocess.run([
                sys.executable, "-c", """
import smbus2
import bme280
try:
    bus = smbus2.SMBus(1)
    address = 0x76
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    print('Sensor BME280 conectado e funcionando!')
except Exception as e:
    print(f'Erro: {e}')
    exit(1)
"""
            ], capture_output=True, text=True, cwd=self.project_dir)
            
            if result.returncode == 0:
                print("Sensor BME280 funcionando")
                print(result.stdout.strip())
                return True
            else:
                print("Sensor BME280 não está funcionando")
                print("   Verifique se o sensor está conectado e I2C está habilitado")
                print("   Execute: sudo raspi-config")
                print("   Interface Options > I2C > Enable")
                return False
                
        except Exception as e:
            print(f"Erro ao verificar sensor: {e}")
            return False
    
    def create_service_file(self):
        """Cria arquivo de serviço systemd"""
        print("Criando serviço systemd...")
        
        service_content = f"""[Unit]
Description=Estacao Meteorologica BME280
After=network.target
Wants=network.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory={self.project_dir}
ExecStart={sys.executable} {self.project_dir}/server.py
PIDFile={self.pid_file}
Restart=always
RestartSec=10
StandardOutput=journal+console
StandardError=journal+console

# Configurações de segurança
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/var/log /var/run {self.project_dir}

# Permissões para acesso ao hardware I2C
SupplementaryGroups=i2c

[Install]
WantedBy=multi-user.target
"""
        
        try:
            with open(self.service_file, 'w') as f:
                f.write(service_content)
            print(f"   {self.service_file}")
            return True
        except Exception as e:
            print(f"   Erro ao criar serviço: {e}")
            return False

    def setup_permissions(self):
        """Configura permissões"""
        print("Configurando permissões...")
        
        try:
            # Adiciona usuário pi ao grupo i2c
            subprocess.run(["usermod", "-a", "-G", "i2c", "pi"], check=True)
            print("   Usuário pi adicionado ao grupo i2c")
            
            # Permissões nos arquivos
            os.chmod(self.project_dir / "server.py", 0o755)
            print("   Permissões do script principal configuradas")
            
            return True
        except Exception as e:
            print(f"   Erro ao configurar permissões: {e}")
            return False
    
    def create_log_file(self):
        """Cria arquivo de log"""
        print("Configurando logs...")
        
        try:
            # Cria arquivo de log
            Path(self.log_file).touch()
            os.chown(self.log_file, 1000, 1000)  # pi:pi
            print(f"   {self.log_file}")
            return True
        except Exception as e:
            print(f"   Erro ao criar log: {e}")
            return False
    
    def enable_service(self):
        """Habilita e inicia o serviço"""
        print("Configurando serviço...")
        
        try:
            # Recarrega systemd
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            print("   systemd recarregado")
            
            # Habilita serviço
            subprocess.run(["systemctl", "enable", "bme280-station.service"], check=True)
            print("   Serviço habilitado para inicialização automática")
            
            # Inicia serviço
            subprocess.run(["systemctl", "start", "bme280-station.service"], check=True)
            print("   Serviço iniciado")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"   Erro ao configurar serviço: {e}")
            return False
    
    def create_control_scripts(self):
        """Cria scripts de controle"""
        print("Criando scripts de controle...")
        
        # Script de controle principal
        control_script = f"""#!/bin/bash
# Script de controle da Estação Meteorológica BME280

case "$1" in
    start)
        sudo systemctl start bme280-station
        ;;
    stop)
        sudo systemctl stop bme280-station
        ;;
    restart)
        sudo systemctl restart bme280-station
        ;;
    status)
        sudo systemctl status bme280-station
        ;;
    logs)
        sudo journalctl -u bme280-station -f
        ;;
    info)
        echo "IP: $(hostname -I)"
        ;;
    *)
        echo "Uso: $0 {{start|stop|restart|status|logs|info}}"
        exit 1
        ;;
esac
"""
        
        try:
            with open(self.project_dir / "station_control.sh", 'w') as f:
                f.write(control_script)
            os.chmod(self.project_dir / "station_control.sh", 0o755)
            print("   station_control.sh")
            
            return True
        except Exception as e:
            print(f"   Erro ao criar scripts: {e}")
            return False

    def display_success_info(self):
        """Exibe informações de sucesso"""
        print("\n" + "="*60)
        print("    INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print()
        print("Comandos úteis:")
        print("   ./station_control.sh start    # Iniciar")
        print("   ./station_control.sh stop     # Parar")
        print("   ./station_control.sh status   # Status")
        print("   ./station_control.sh logs     # Ver logs")
        print("   ./station_control.sh info     # Ver IP")
        print()
        print("O serviço será iniciado automaticamente no boot!")
        print("="*60)
        print()
    
    def install(self):
        """Executa instalação completa"""
        self.print_header()
        
        if not self.check_root():
            return False
        
        steps = [
            ("Verificando dependências", self.check_dependencies),
            ("Verificando sensor", self.check_sensor),
            ("Criando serviço systemd", self.create_service_file),
            ("Configurando permissões", self.setup_permissions),
            ("Configurando logs", self.create_log_file),
            ("Configurando serviço", self.enable_service),
            ("Criando scripts de controle", self.create_control_scripts)
        ]
        
        for step_name, step_func in steps:
            print(f"\n{step_name}...")
            if not step_func():
                print(f"\nFalha na etapa: {step_name}")
                return False
        
        self.display_success_info()
        return True


def main():
    """Função principal"""
    installer = BME280Installer()

    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        # Desinstalação
        print("Desinstalando estação meteorológica...")
        subprocess.run(["systemctl", "stop", "bme280-station"], check=False)
        subprocess.run(["systemctl", "disable", "bme280-station"], check=False)
        subprocess.run(["rm", "-f", "/etc/systemd/system/bme280-station.service"], check=False)
        subprocess.run(["systemctl", "daemon-reload"], check=False)
        print("Desinstalação concluída!")
    else:
        # Instalação
        installer.install()

if __name__ == "__main__":
    main()
