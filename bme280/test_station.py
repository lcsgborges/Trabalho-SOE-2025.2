#!/usr/bin/env python3
"""
Script de teste para a estação BME280
Testa se o script principal pode rodar sem problemas de permissão.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_permissions():
    """Testa permissões dos diretórios"""
    base_dir = Path(__file__).parent.absolute()
    
    print("Testando permissões...")
    print(f"Diretório base: {base_dir}")
    
    # Testa diretório de logs
    log_dir = base_dir / 'logs'
    if not log_dir.exists():
        print(f"Criando diretório de logs: {log_dir}")
        log_dir.mkdir(exist_ok=True)
    
    # Testa escrita no arquivo de log
    log_file = log_dir / 'test.log'
    try:
        with open(log_file, 'w') as f:
            f.write("Teste de escrita\n")
        print(f"✓ Consegue escrever em: {log_file}")
        log_file.unlink()  # Remove arquivo de teste
    except PermissionError as e:
        print(f"✗ Erro de permissão: {e}")
        return False
    
    return True

def test_imports():
    """Testa imports necessários"""
    print("\nTestando imports...")
    
    try:
        import smbus2
        print("✓ smbus2 importado com sucesso")
    except ImportError:
        print("✗ smbus2 não encontrado - execute: pip install --break-system-packages smbus2")
        return False
    
    try:
        import bme280
        print("✓ bme280 importado com sucesso")
    except ImportError:
        print("✗ bme280 não encontrado - execute: pip install --break-system-packages RPi.bme280")
        return False
    
    try:
        from flask import Flask
        print("✓ Flask importado com sucesso")
    except ImportError:
        print("✗ Flask não encontrado - execute: pip install --break-system-packages Flask")
        return False
    
    return True

def test_station():
    """Testa a inicialização da estação"""
    print("\nTestando inicialização da estação...")
    
    try:
        from bme280_station import BME280Station
        station = BME280Station()
        print("✓ BME280Station criada com sucesso")
        print(f"✓ Arquivo de log configurado: {station.config['log_file']}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar estação: {e}")
        return False

def main():
    """Função principal de teste"""
    print("="*50)
    print("TESTE DA ESTAÇÃO METEOROLÓGICA BME280")
    print("="*50)
    
    tests = [
        ("Permissões", test_permissions),
        ("Imports", test_imports),
        ("Estação", test_station)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        if not test_func():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("✓ TODOS OS TESTES PASSARAM!")
        print("A estação está pronta para funcionar.")
    else:
        print("✗ ALGUNS TESTES FALHARAM!")
        print("Corrija os problemas antes de continuar.")
    print("="*50)

if __name__ == "__main__":
    main()