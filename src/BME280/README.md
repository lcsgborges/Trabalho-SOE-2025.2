# Guia de Utilização

## Instalação Rápida (1 comando)

```bash
# Na Raspberry Pi, execute:
cd /home/pi/trabalho/src/BME280
chmod +x setup_rpi.sh
./setup_rpi.sh
sudo reboot
```

**Pronto!** Após reiniciar, o servidor estará rodando automaticamente.

## Como Acessar

### No navegador (de qualquer dispositivo na mesma rede):

```bash
http://<IP_DA_RPI>:8080
```

### Descobrir o IP da Raspberry Pi

```bash
hostname -I
```

OU execute:

```bash
./start_server.sh
```

## Comandos Úteis

```bash
# Ver status do serviço
sudo systemctl status bme280

# Ver logs em tempo real
sudo journalctl -u bme280 -f

# Parar o servidor
sudo systemctl stop bme280

# Iniciar o servidor
sudo systemctl start bme280

# Desabilitar início automático
sudo systemctl disable bme280

# Ver logs do servidor
tail -f /tmp/bme280.log
```

## Verificar Sensor

```bash
# Detectar BME280
sudo i2cdetect -y 1

# Deve mostrar: 76 ou 77
```

## Execução Manual (sem systemd)

```bash
cd /home/pi/trabalho/src/BME280
./start_server.sh
```
