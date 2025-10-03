#!/usr/bin/env python3
"""
Script de diagnóstico do sensor BME280
Testa especificamente a conexão e leitura do sensor.
"""

import sys
import time
from datetime import datetime

def test_i2c_devices():
    """Testa se existem dispositivos I2C"""
    print("=== TESTE I2C ===")
    try:
        import smbus2
        bus = smbus2.SMBus(1)
        
        # Testa endereços comuns do BME280
        addresses = [0x76, 0x77]
        found_devices = []
        
        for addr in addresses:
            try:
                bus.read_byte(addr)
                found_devices.append(hex(addr))
                print(f"✓ Dispositivo encontrado no endereço {hex(addr)}")
            except:
                print(f"✗ Nenhum dispositivo no endereço {hex(addr)}")
        
        bus.close()
        return found_devices
        
    except Exception as e:
        print(f"✗ Erro ao acessar I2C: {e}")
        return []

def test_bme280_sensor(address=0x76):
    """Testa especificamente o sensor BME280"""
    print(f"\n=== TESTE SENSOR BME280 (endereço {hex(address)}) ===")
    
    try:
        import smbus2
        import bme280
        
        # Inicializa o sensor
        bus = smbus2.SMBus(1)
        calibration_params = bme280.load_calibration_params(bus, address)
        print("✓ Parâmetros de calibração carregados")
        
        # Faz 3 leituras de teste
        for i in range(3):
            print(f"\n--- Leitura {i+1} ---")
            data = bme280.sample(bus, address, calibration_params)
            
            print(f"Temperatura: {data.temperature:.2f}°C")
            print(f"Pressão: {data.pressure:.2f} hPa")
            print(f"Umidade: {data.humidity:.2f}%")
            print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if i < 2:  # Não espera após a última leitura
                time.sleep(2)
        
        bus.close()
        print("\n✓ Sensor BME280 funcionando perfeitamente!")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao testar sensor BME280: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

def test_station_data_flow():
    """Testa o fluxo de dados da estação"""
    print(f"\n=== TESTE FLUXO DE DADOS DA ESTAÇÃO ===")
    
    try:
        from bme280_station import BME280Station
        
        # Cria uma instância da estação
        station = BME280Station()
        print("✓ Estação criada")
        
        # Testa inicialização do sensor
        if station.init_sensor():
            print("✓ Sensor inicializado na estação")
            
            # Faz uma coleta manual de dados
            try:
                data = bme280.sample(station.bus, station.config['sensor_address'], station.calibration_params)
                station.sensor_data.update({
                    'temperature': round(data.temperature, 2),
                    'pressure': round(data.pressure, 2),
                    'humidity': round(data.humidity, 2),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'online'
                })
                
                print("✓ Dados coletados manualmente:")
                print(f"  - Temperatura: {station.sensor_data['temperature']}°C")
                print(f"  - Pressão: {station.sensor_data['pressure']} hPa")
                print(f"  - Umidade: {station.sensor_data['humidity']}%")
                print(f"  - Status: {station.sensor_data['status']}")
                
                station.bus.close()
                return True
                
            except Exception as e:
                print(f"✗ Erro na coleta manual: {e}")
                return False
        else:
            print("✗ Falha na inicialização do sensor na estação")
            return False
            
    except Exception as e:
        print(f"✗ Erro ao testar estação: {e}")
        return False

def main():
    """Função principal de diagnóstico"""
    print("="*60)
    print("DIAGNÓSTICO COMPLETO DO SENSOR BME280")
    print("="*60)
    
    # Teste 1: Dispositivos I2C
    found_devices = test_i2c_devices()
    
    if not found_devices:
        print("\n❌ FALHA CRÍTICA: Nenhum dispositivo I2C encontrado")
        print("Verifique:")
        print("1. Se o I2C está habilitado: sudo raspi-config")
        print("2. Se o sensor está conectado corretamente")
        print("3. Se os fios estão bem conectados (VCC, GND, SDA, SCL)")
        return
    
    # Teste 2: Sensor BME280
    sensor_working = False
    for device_addr_str in found_devices:
        device_addr = int(device_addr_str, 16)
        if test_bme280_sensor(device_addr):
            sensor_working = True
            break
    
    if not sensor_working:
        print("\n❌ FALHA: Sensor BME280 não está respondendo corretamente")
        return
    
    # Teste 3: Fluxo de dados da estação
    if test_station_data_flow():
        print("\n✅ SUCESSO: Todos os testes passaram!")
        print("O sensor deve funcionar corretamente na estação.")
    else:
        print("\n❌ FALHA: Problema no fluxo de dados da estação")
    
    print("="*60)

if __name__ == "__main__":
    main()