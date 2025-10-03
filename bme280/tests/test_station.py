#!/usr/bin/env python3
"""
Teste do sistema da estação BME280
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Testa se as dependências estão instaladas"""
    print("Testando dependências...")
    
    modules = ['smbus2', 'bme280', 'flask']
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} não encontrado")
            return False
    return True

def test_station():
    """Testa se a estação inicializa"""
    print("\nTestando estação...")
    
    try:
        from bme280_station import BME280Station
        station = BME280Station()
        print("✓ Estação criada")
        return True
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=== TESTE DO SISTEMA ===")
    
    if test_imports() and test_station():
        print("\n✓ Sistema OK")
    else:
        print("\n✗ Sistema com problemas")

if __name__ == "__main__":
    main()