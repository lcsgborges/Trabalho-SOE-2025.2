#!/usr/bin/env python3
"""
Estação Meteorológica BME280 - Sistema Simplificado
Sistema básico de monitoramento meteorológico com controle simples.
"""

import os
import sys
import time
import signal
import threading
from datetime import datetime

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
        
        # Configurações básicas
        self.config = {
            'sensor_address': 0x76,
            'i2c_bus': 1,
            'collect_interval': 60,  # segundos
            'server_host': '0.0.0.0',
            'server_port': 5000
        }
        
        # Dados do sensor
        self.sensor_data = {
            'temperature': 0,
            'pressure': 0,
            'humidity': 0,
            'timestamp': '',
            'status': 'offline'
        }
        
        # Configurar rotas do Flask
        self.setup_routes()
        
        # Configurar sinais para shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def setup_routes(self):
        """Configura as rotas básicas do Flask"""
        
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
        
        @self.app.route('/api/start')
        def start_sensor():
            """Inicia a coleta de dados do sensor"""
            if not self.running:
                success = self.start_sensor_collection()
                return jsonify({'success': success, 'message': 'Sensor iniciado' if success else 'Erro ao iniciar sensor'})
            return jsonify({'success': False, 'message': 'Sensor já está rodando'})
        
        @self.app.route('/api/stop')
        def stop_sensor():
            """Para a coleta de dados do sensor"""
            if self.running:
                self.stop_sensor_collection()
                return jsonify({'success': True, 'message': 'Sensor parado'})
            return jsonify({'success': False, 'message': 'Sensor não está rodando'})
    
    def init_sensor(self):
        """Inicializa o sensor BME280"""
        try:
            print(f"Conectando ao barramento I2C {self.config['i2c_bus']}")
            self.bus = smbus2.SMBus(self.config['i2c_bus'])
            
            print(f"Carregando parâmetros do sensor no endereço {hex(self.config['sensor_address'])}")
            self.calibration_params = bme280.load_calibration_params(
                self.bus, self.config['sensor_address']
            )
            
            # Testa uma leitura
            test_data = bme280.sample(self.bus, self.config['sensor_address'], self.calibration_params)
            print(f"Sensor OK: T={test_data.temperature:.1f}°C, P={test_data.pressure:.1f}hPa, U={test_data.humidity:.1f}%")
            return True
        except Exception as e:
            print(f"Erro no endereço 0x76: {e}")
            # Tenta endereço alternativo
            if self.config['sensor_address'] == 0x76:
                print("Tentando endereço 0x77...")
                try:
                    self.config['sensor_address'] = 0x77
                    self.calibration_params = bme280.load_calibration_params(
                        self.bus, self.config['sensor_address']
                    )
                    test_data = bme280.sample(self.bus, self.config['sensor_address'], self.calibration_params)
                    print(f"Sensor encontrado em 0x77! T={test_data.temperature:.1f}°C")
                    return True
                except Exception as e2:
                    print(f"Erro no endereço 0x77: {e2}")
            return False
    
    def collect_sensor_data(self):
        """Coleta dados do sensor em loop"""
        print("Iniciando coleta de dados...")
        while self.running:
            try:
                data = bme280.sample(self.bus, self.config['sensor_address'], self.calibration_params)
                self.sensor_data.update({
                    'temperature': round(data.temperature, 1),
                    'pressure': round(data.pressure, 1),
                    'humidity': round(data.humidity, 1),
                    'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                    'status': 'online'
                })
                print(f"Dados: T={self.sensor_data['temperature']}°C P={self.sensor_data['pressure']}hPa U={self.sensor_data['humidity']}%")
            except Exception as e:
                self.sensor_data.update({
                    'status': 'error',
                    'error_message': str(e),
                    'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                })
                print(f"Erro na coleta: {e}")
            
            time.sleep(self.config['collect_interval'])
        
        print("Coleta de dados finalizada")
    
    def start_sensor_collection(self):
        """Inicia coleta de dados do sensor"""
        if not self.init_sensor():
            print("Falha na inicialização do sensor")
            return False
        
        self.running = True
        self.sensor_thread = threading.Thread(target=self.collect_sensor_data, daemon=True)
        self.sensor_thread.start()
        print("Coleta de dados iniciada")
        return True
    
    def stop_sensor_collection(self):
        """Para a coleta de dados do sensor"""
        self.running = False
        self.sensor_data['status'] = 'offline'
        print("Coleta de dados parada")
    
    def signal_handler(self, signum, frame):
        """Manipula sinais de parada"""
        print(f"Recebido sinal para parar...")
        self.stop()
    
    def stop(self):
        """Para a estação meteorológica"""
        self.running = False
        print("Estação parada")
    
    def run(self):
        """Executa apenas o servidor web"""
        print("="*50)
        print("   ESTAÇÃO METEOROLÓGICA BME280 - BÁSICA")
        print("="*50)
        print(f"Servidor: http://localhost:{self.config['server_port']}")
        print("Use os botões na interface para controlar o sensor")
        print("Pressione Ctrl+C para parar")
        print("="*50)
        
        try:
            self.app.run(
                host=self.config['server_host'],
                port=self.config['server_port'],
                debug=False
            )
        except KeyboardInterrupt:
            print("\nParando servidor...")
        finally:
            self.stop()

def main():
    """Função principal"""
    station = BME280Station()
    station.run()

if __name__ == '__main__':
    main()
