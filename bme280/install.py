#!/usr/bin/env python3
"""
Instalador BME280 - Versão Simplificada
"""

import os
import sys
import subprocess
from pathlib import Path

def check_root():
    """Verifica se está rodando como root"""
    if os.geteuid() != 0:
        print("Execute como root: sudo python3 install.py")
        return False
    return True
    
def install_dependencies():
    """Instala dependências"""
    print("Instalando dependências...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", "requirements.txt"], check=True)
        print("✓ Dependências instaladas")
        return True
    except:
        print("✗ Erro ao instalar dependências")
        return False

def create_service():
    """Cria serviço systemd"""
    print("Criando serviço...")
    
    project_dir = Path(__file__).parent.absolute()
    service_content = f"""[Unit]
Description=BME280 Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory={project_dir}
ExecStart={sys.executable} {project_dir}/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    try:
        with open("/etc/systemd/system/bme280-station.service", 'w') as f:
            f.write(service_content)
        print("✓ Serviço criado")
        return True
    except:
        print("✗ Erro ao criar serviço")
        return False

def setup_permissions():
    """Configura permissões"""
    print("Configurando permissões...")
    try:
        subprocess.run(["usermod", "-a", "-G", "i2c", "pi"], check=True)
        os.chmod("server.py", 0o755)
        print("✓ Permissões configuradas")
        return True
    except:
        print("✗ Erro nas permissões")
        return False

def enable_service():
    """Habilita serviço"""
    print("Habilitando serviço...")
    try:
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", "bme280-station.service"], check=True)
        subprocess.run(["systemctl", "start", "bme280-station.service"], check=True)
        print("✓ Serviço habilitado e iniciado")
        return True
    except:
        print("✗ Erro ao habilitar serviço")
        return False

def create_control_script():
    """Cria script de controle"""
    print("Criando script de controle...")
    
    script_content = """#!/bin/bash
case "$1" in
    start)   sudo systemctl start bme280-station ;;
    stop)    sudo systemctl stop bme280-station ;;
    restart) sudo systemctl restart bme280-station ;;
    status)  sudo systemctl status bme280-station ;;
    logs)    sudo journalctl -u bme280-station -f ;;
    *)       echo "Uso: $0 {start|stop|restart|status|logs}" ;;
esac
"""
    
    try:
        with open("station_control.sh", 'w') as f:
            f.write(script_content)
        os.chmod("station_control.sh", 0o755)
        print("✓ Script de controle criado")
        return True
    except:
        print("✗ Erro ao criar script")
        return False

def install():
    """Instala o sistema"""
    print("=== INSTALADOR BME280 ===")
    
    if not check_root():
        return False
    
    steps = [
        install_dependencies,
        create_service,
        setup_permissions,
        enable_service,
        create_control_script
    ]
    
    for step in steps:
        if not step():
            print("✗ Instalação falhou")
            return False
    
    print("\n✓ INSTALAÇÃO CONCLUÍDA!")
    print("Acesse: http://localhost:5000")
    print("Controle: ./station_control.sh start|stop|status")
    return True

def uninstall():
    """Desinstala o sistema"""
    print("Desinstalando...")
    subprocess.run(["systemctl", "stop", "bme280-station"], check=False)
    subprocess.run(["systemctl", "disable", "bme280-station"], check=False)
    subprocess.run(["rm", "-f", "/etc/systemd/system/bme280-station.service"], check=False)
    subprocess.run(["systemctl", "daemon-reload"], check=False)
    print("✓ Desinstalação concluída")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall()
    else:
        install()
