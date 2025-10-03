# Estação Meteorológica - BME 280

Sistema para monitoramento de temperatura, pressão e umidade usando o sensor BME280.

## Instalação

```bash
cd bme280/
sudo python3 install.py
```

## Uso

### Controle

```bash
./station_control.sh start    # Iniciar
./station_control.sh stop     # Parar
./station_control.sh status   # Status
./station_control.sh logs     # Ver logs
```

### Interface Web

- **Local**: http://localhost:5000
- **Remoto**: http://[IP_DA_PI]:5000

### API

```bash
curl http://localhost:5000/api/data      # Dados
curl http://localhost:5000/api/status    # Status
```

## Arquivos

``` bash
bme280/
├── server.py            # Script principal
├── install.py           # Instalador
├── station_control.sh   # Controle
├── requirements.txt     # Dependências
└── templates/           # Interface web
```
