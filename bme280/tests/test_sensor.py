#!/usr/bin/env python3
"""
Teste do sensor BME280
"""

def test_sensor():
    """Testa o sensor BME280"""
    print("Testando sensor BME280...")
    
    try:
        import smbus2
        import bme280
        
        # Testa endereços comuns
        for addr in [0x76, 0x77]:
            try:
                bus = smbus2.SMBus(1)
                params = bme280.load_calibration_params(bus, addr)
                data = bme280.sample(bus, addr, params)
                
                print(f"✓ Sensor encontrado em {hex(addr)}")
                print(f"  Temperatura: {data.temperature:.1f}°C")
                print(f"  Pressão: {data.pressure:.0f}hPa")
                print(f"  Umidade: {data.humidity:.0f}%")
                
                bus.close()
                return True
                
            except:
                continue
        
        print("✗ Sensor não encontrado")
        return False
        
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

if __name__ == "__main__":
    test_sensor()