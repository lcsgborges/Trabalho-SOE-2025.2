#!/usr/bin/env python3
"""
Estação Meteorológica BME280 - Sistema Unificado
Sistema completo de monitoramento meteorológico com servidor web e inicialização automática.
"""

import os
import sys
import time
import signal
import logging
import threading
import subprocess
from datetime import datetime
from pathlib import Path

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports do sensor e servidor
try:
    import smbus2
    import bme280
    from flask import Flask, render_template, jsonify
except ImportError as e:
    print(f"Erro ao importar dependências: {e}")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

class BME280Station:
    """Classe principal da estação meteorológica BME280"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.running = False
        self.sensor_thread = None
        self.server_thread = None
        
        # Diretório base do projeto
        self.base_dir = Path(__file__).parent.absolute()
        
        # Configurações
        self.config = {
            'sensor_address': 0x76,
            'i2c_bus': 1,
            'collect_interval': 60,  # segundos
            'server_host': '0.0.0.0',
            'server_port': 5000,
            'log_file': str(self.base_dir / 'logs' / 'bme280.log'),
            'pid_file': '/var/run/bme280-station.pid'
        }
        
        # Dados do sensor
        self.sensor_data = {
            'temperature': 0,
            'pressure': 0,
            'humidity': 0,
            'timestamp': '',
            'status': 'offline'
        }
        
        # Configurar logging
        self.setup_logging()
        
        # Configurar rotas do Flask
        self.setup_routes()
        
        # Configurar sinais para shutdown graceful
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def setup_logging(self):
        """Configura o sistema de logging"""
        # Criar diretório de logs se não existir
        log_dir = self.base_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        # Configurar permissões do diretório de logs
        try:
            os.chmod(log_dir, 0o755)
        except:
            pass  # Ignora erro de permissão se não for possível alterar
        
        # Configurar handlers de logging
        handlers = [logging.StreamHandler()]
        
        # Tenta criar handler de arquivo, se falhar usa apenas console
        try:
            file_handler = logging.FileHandler(self.config['log_file'])
            handlers.append(file_handler)
        except PermissionError:
            print(f"Aviso: Não foi possível criar log em {self.config['log_file']}")
            print("Usando apenas saída do console")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_routes(self):
        """Configura as rotas do Flask"""
        
        @self.app.route('/')
        def index():
            return render_template('dashboard.html')
        
        @self.app.route('/api/data')
        def get_data():
            return jsonify(self.sensor_data)
        
        @self.app.route('/api/status')
        def get_status():
            return jsonify({
                'status': self.sensor_data['status'],
                'last_update': self.sensor_data['timestamp'],
                'server_running': self.running
            })
        
        @self.app.route('/api/info')
        def get_info():
            return jsonify({
                'station_name': 'Estação Meteorológica BME280',
                'version': '1.0.0',
                'sensor_interval': self.config['collect_interval'],
                'server_url': f"http://{self.get_local_ip()}:{self.config['server_port']}"
            })
    
    def get_local_ip(self):
        """Obtém o IP local da máquina"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return "localhost"
    
    def init_sensor(self):
        """Inicializa o sensor BME280"""
        try:
            self.bus = smbus2.SMBus(self.config['i2c_bus'])
            self.calibration_params = bme280.load_calibration_params(
                self.bus, self.config['sensor_address']
            )
            self.logger.info("Sensor BME280 inicializado com sucesso")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao inicializar sensor: {e}")
            return False
    
    def collect_sensor_data(self):
        """Coleta dados do sensor em loop"""
        while self.running:
            try:
                data = bme280.sample(self.bus, self.config['sensor_address'], self.calibration_params)
                self.sensor_data.update({
                    'temperature': round(data.temperature, 2),
                    'pressure': round(data.pressure, 2),
                    'humidity': round(data.humidity, 2),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'online'
                })
                self.logger.info(f"Dados coletados: T={self.sensor_data['temperature']}°C, "
                               f"P={self.sensor_data['pressure']}hPa, "
                               f"U={self.sensor_data['humidity']}%")
            except Exception as e:
                self.sensor_data.update({
                    'status': 'error',
                    'error_message': str(e),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                self.logger.error(f"Erro na coleta de dados: {e}")
            
            time.sleep(self.config['collect_interval'])
    
    def start_sensor_thread(self):
        """Inicia thread de coleta de dados"""
        if not self.init_sensor():
            return False
        
        self.sensor_thread = threading.Thread(target=self.collect_sensor_data, daemon=True)
        self.sensor_thread.start()
        self.logger.info("Thread de coleta de dados iniciada")
        return True
    
    def start_server(self):
        """Inicia o servidor Flask"""
        try:
            self.app.run(
                host=self.config['server_host'],
                port=self.config['server_port'],
                debug=False,
                use_reloader=False,
                threaded=True
            )
        except Exception as e:
            self.logger.error(f"Erro ao iniciar servidor: {e}")
    
    def start_server_thread(self):
        """Inicia servidor em thread separada"""
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()
        self.logger.info("Servidor Flask iniciado")
    
    def display_startup_info(self):
        """Exibe informações de inicialização"""
        local_ip = self.get_local_ip()
        
        print("\n" + "="*60)
        print("           ESTAÇÃO METEOROLÓGICA BME280")
        print("="*60)
        print(f"IP da Raspberry Pi: {local_ip}")
        print(f"Servidor: http://{local_ip}:{self.config['server_port']}")
        print(f"API de dados: http://{local_ip}:{self.config['server_port']}/api/data")
        print(f"Status: http://{local_ip}:{self.config['server_port']}/api/status")
        print(f"Coleta de dados: A cada {self.config['collect_interval']} segundos")
        print("="*60)
        print("Pressione Ctrl+C para parar")
        print("="*60 + "\n")
    
    def signal_handler(self, signum, frame):
        """Manipula sinais de parada"""
        self.logger.info(f"Recebido sinal {signum}, parando estação...")
        self.stop()
    
    def stop(self):
        """Para a estação meteorológica"""
        self.running = False
        self.logger.info("Estação meteorológica parada")
    
    def run(self):
        """Executa a estação meteorológica"""
        self.logger.info("Iniciando Estação Meteorológica BME280...")
        
        # Inicia coleta de dados
        if not self.start_sensor_thread():
            self.logger.error("Falha ao inicializar sensor, parando...")
            return False
        
        # Inicia servidor web
        self.start_server_thread()
        
        # Aguarda um pouco para o servidor inicializar
        time.sleep(2)
        
        # Exibe informações
        self.display_startup_info()
        
        # Marca como rodando
        self.running = True
        
        # Salva PID se estiver rodando como serviço
        if os.geteuid() == 0:  # Se rodando como root
            try:
                with open(self.config['pid_file'], 'w') as f:
                    f.write(str(os.getpid()))
            except:
                pass
        
        try:
            # Loop principal
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Interrompido pelo usuário")
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Limpeza ao parar"""
        self.running = False
        
        # Remove arquivo PID
        try:
            if os.path.exists(self.config['pid_file']):
                os.remove(self.config['pid_file'])
        except:
            pass
        
        self.logger.info("Limpeza concluída")

def main():
    """Função principal"""
    station = BME280Station()
    
    # Verifica argumentos da linha de comando
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'start':
            station.run()
        elif command == 'stop':
            # Para o serviço se estiver rodando
            try:
                with open(station.config['pid_file'], 'r') as f:
                    pid = int(f.read().strip())
                os.kill(pid, signal.SIGTERM)
                print("Estação parada")
            except:
                print("Estação não estava rodando")
        elif command == 'status':
            try:
                with open(station.config['pid_file'], 'r') as f:
                    pid = int(f.read().strip())
                os.kill(pid, 0)  # Verifica se processo existe
                print("Estação rodando")
            except:
                print("Estação não está rodando")
        elif command == 'info':
            print(f"IP: {station.get_local_ip()}")
            print(f"URL: http://{station.get_local_ip()}:{station.config['server_port']}")
        else:
            print("Uso: python3 bme280_station.py [start|stop|status|info]")
    else:
        # Executa normalmente
        station.run()

if __name__ == '__main__':
    main()
