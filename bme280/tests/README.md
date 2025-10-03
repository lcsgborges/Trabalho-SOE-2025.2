# Pasta de Testes - Estação Meteorológica BME280

Esta pasta contém arquivos de teste e diagnóstico para o sistema da estação meteorológica.

## Arquivos de Teste

### `diagnose_sensor.py`
Script de diagnóstico completo para o sensor BME280:
- Verifica conexão I2C
- Testa comunicação com o sensor
- Valida calibração
- Testa leitura de dados
- Verifica configurações do sistema

**Uso:**
```bash
python3 diagnose_sensor.py
```

### `test_station.py`
Script de teste para o sistema da estação:
- Testa inicialização do sistema
- Verifica configurações
- Testa APIs
- Valida funcionamento geral

**Uso:**
```bash
python3 test_station.py
```

## Como Executar os Testes

### 1. Ativar ambiente virtual
```bash
cd /home/pi/Faculdade/Trabalhos/trabalho-soe/bme280
source venv/bin/activate
```

### 2. Executar diagnóstico do sensor
```bash
cd tests
python3 diagnose_sensor.py
```

### 3. Executar testes do sistema
```bash
python3 test_station.py
```
