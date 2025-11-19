# Servidor BME280 para Raspberry Pi 3 Model B

Sistema de monitoramento de temperatura, pressão e umidade usando sensor BME280 com interface web em tempo real.

## Requisitos

- Raspberry Pi 3 Model B
- Sensor BME280 conectado via I2C

## Instalação Rápida

Na Raspberry Pi, execute:

```bash
cd /home/pi/trabalho/src/BME280
chmod +x setup_rpi.sh
./setup_rpi.sh
sudo reboot
```

Após reiniciar, o servidor estará rodando automaticamente e pode ser acessado pela rede.

## Acesso ao Dashboard

No navegador de qualquer dispositivo na mesma rede:

```bash
http://<IP_DA_RPI>:8080
```

Para descobrir o IP da Raspberry Pi:

```bash
hostname -I
```

## Scripts Disponíveis

### setup_rpi.sh

Script de instalação e configuração inicial do sistema.

Uso:

```bash
./setup_rpi.sh
```

### start_server.sh

Inicia o servidor BME280 em modo background.

Uso:

```bash
./start_server.sh
```

### check_status.sh

Verifica o status de execução do servidor.

Uso:

```bash
./check_status.sh
```

### stop_and_clean.sh

Para o servidor e limpa arquivos.

Uso:

```bash
./stop_and_clean.sh
```

### clear_csv.sh

Remove apenas o arquivo CSV de dados.

Uso:

```bash
./clear_csv.sh
```

## Gerenciamento do Serviço (systemd)

O servidor é configurado como serviço systemd para iniciar automaticamente no boot.

```bash
# Ver status do serviço
sudo systemctl status bme280

# Parar o servidor
sudo systemctl stop bme280

# Iniciar o servidor
sudo systemctl start bme280

# Reiniciar o servidor
sudo systemctl restart bme280

# Desabilitar início automático
sudo systemctl disable bme280

# Habilitar início automático
sudo systemctl enable bme280

# Ver logs do serviço
sudo journalctl -u bme280 -f
```

## Verificação do Sensor I2C

```bash
# Detectar dispositivos I2C
sudo i2cdetect -y 1

# O sensor BME280 deve aparecer em 0x76 ou 0x77
```

## Configurações Importantes

### Horário

Os dados são salvos com horário de Brasília (UTC-3).

### Intervalo de Leitura

O sensor é lido a cada 10 segundos (configurável no main.cpp).

### Atualização da Interface

A página web atualiza automaticamente a cada 10 segundos.

### Máximo de Linhas Exibidas

A tabela mostra as últimas 15 medições (configurável em script.js).

## Credenciais da Raspberry Pi

```txt
Usuário: pi
Senha: (sem senha, apenas pressionar Enter)
```
