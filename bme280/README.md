# Estação Meteorológica BME280 - Sistema Unificado

Sistema completo e modularizado de monitoramento meteorológico usando sensor BME280, servidor web Flask e inicialização automática na Raspberry Pi.

## Visão Geral

Este projeto implementa uma estação meteorológica completa e modularizada que:
- Coleta dados de temperatura, pressão e umidade a cada minuto
- Exibe dados em tempo real via interface web responsiva
- Inicia automaticamente no boot da Raspberry Pi
- Permite acesso remoto de outros dispositivos na rede
- Sistema robusto com logs e reinicialização automática
- **Arquitetura modular e unificada** - tudo em um sistema integrado


## Instalação Rápida

### 1. Instalar o Sistema Completo
```bash
cd /home/pi/Faculdade/Trabalhos/trabalho-soe/bme280
sudo python3 install.py
```

### 2. Verificar Instalação
```bash
./station_control.sh status
```

### 3. Reiniciar a Raspberry Pi
```bash
sudo reboot
```

**Pronto!** O sistema estará rodando automaticamente após o reboot.

## Uso

### Controle da Estação
```bash
# Iniciar estação
./station_control.sh start

# Parar estação
./station_control.sh stop

# Reiniciar estação
./station_control.sh restart

# Ver status
./station_control.sh status

# Ver logs em tempo real
./station_control.sh logs

# Ver informações (IP, URL)
./station_control.sh info

# Testar sensor
./station_control.sh test

# Instalar sistema
./station_control.sh install

# Desinstalar sistema
./station_control.sh uninstall
```

### Interface Web
- **Acesso local**: `http://localhost:5000`
- **Acesso remoto**: `http://[IP_DA_RASPBERRY]:5000`
- **Dashboard responsivo**: Funciona em desktop e mobile
- **Atualização automática**: Interface atualiza a cada 10 segundos

### API Endpoints

#### Obter dados atuais
```bash
curl http://localhost:5000/api/data
```

Resposta:
```json
{
  "temperature": 23.45,
  "pressure": 1013.25,
  "humidity": 65.30,
  "timestamp": "2024-01-15 14:30:00",
  "status": "online"
}
```

#### Verificar status
```bash
curl http://localhost:5000/api/status
```

#### Informações da estação
```bash
curl http://localhost:5000/api/info
```

## Estrutura do Projeto

```
bme280/
├── bme280_station.py          # Script principal unificado
├── install.py                 # Instalador do sistema
├── station_control.sh         # Script de controle
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
├── config/
│   └── station_config.py      # Configurações centralizadas
├── templates/
│   └── dashboard.html         # Interface web
├── scripts/                   # Scripts auxiliares (vazios)
└── logs/                      # Logs do sistema
```

## Configuração

### Arquivo de Configuração
Todas as configurações estão centralizadas em `config/station_config.py`:

```python
# Configurações do Sensor
SENSOR_CONFIG = {
    'address': 0x76,           # Endereço I2C
    'i2c_bus': 1,              # Barramento I2C
    'collect_interval': 60,    # Intervalo de coleta (segundos)
}

# Configurações do Servidor
SERVER_CONFIG = {
    'host': '0.0.0.0',         # Host do servidor
    'port': 5000,              # Porta do servidor
    'debug': False,            # Modo debug
}
```

### Modificar Configurações
1. Edite `config/station_config.py`
2. Reinicie a estação: `./station_control.sh restart`

## Solução de Problemas

### Verificar Status
```bash
./station_control.sh status
```

### Ver Logs
```bash
./station_control.sh logs
```

### Testar Sensor
```bash
./station_control.sh test
```

### Problemas Comuns

#### Serviço não inicia
```bash
# Verificar logs de erro
sudo journalctl -u bme280-station --no-pager -l

# Verificar se o sensor está conectado
./station_control.sh test
```

#### Sensor não detectado
```bash
# Verificar se I2C está habilitado
sudo raspi-config
# Interface Options > I2C > Enable

# Verificar dispositivos I2C
sudo i2cdetect -y 1
```

#### Erro de permissão
```bash
# Adicionar usuário ao grupo i2c
sudo usermod -a -G i2c pi
# Reiniciar o sistema
```

#### Porta já em uso
```bash
# Verificar processos na porta 5000
sudo lsof -i :5000
# Matar processo se necessário
sudo kill -9 <PID>
```

## Descoberta de IP para Acesso Remoto

### Descobrir IP automaticamente
```bash
./station_control.sh info
```

### Comando manual
```bash
hostname -I
```

## Desinstalação

### Remover Sistema Completo
```bash
./station_control.sh uninstall
```

### Remover Manualmente
```bash
sudo systemctl stop bme280-station
sudo systemctl disable bme280-station
sudo rm -f /etc/systemd/system/bme280-station.service
sudo systemctl daemon-reload
```

## Arquivos do Sistema

Após a instalação, os seguintes arquivos são criados:
- `/etc/systemd/system/bme280-station.service` - Configuração do serviço
- `/var/log/bme280-station.log` - Log do sistema
- `/var/run/bme280-station.pid` - PID do processo

## Próximos Passos

Após configurar a inicialização automática, você pode:
- Configurar acesso remoto via VPN
- Implementar notificações por email
- Adicionar monitoramento de sistema
- Configurar backup automático dos dados
- Implementar alertas de falha
- Adicionar histórico de dados
- Implementar gráficos de tendência
