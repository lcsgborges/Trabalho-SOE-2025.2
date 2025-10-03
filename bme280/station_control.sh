#!/bin/bash
# Script de controle da Estação Meteorológica BME280

case "$1" in
    start)
        sudo systemctl start bme280-station
        ;;
    stop)
        sudo systemctl stop bme280-station
        ;;
    restart)
        sudo systemctl restart bme280-station
        ;;
    status)
        sudo systemctl status bme280-station
        ;;
    logs)
        sudo journalctl -u bme280-station -f
        ;;
    info)
        python3 /home/pi/trabalho/bme280/bme280_station.py info
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|status|logs|info}"
        exit 1
        ;;
esac
