#include "SensorBME280.h"
#include <iostream>
#include <unistd.h>

int main() {
    SensorBME280 sensor;

    if (!sensor.begin()) {
        std::cout << "Falha ao iniciar BME280" << std::endl;
        return 1;
    }

    while (true) {
        float temp = sensor.readTemperature();
        float press = sensor.readPressure();
        float hum = sensor.readHumidity();

        std::cout << "Temperatura: " << temp << " °C" << std::endl;
        std::cout << "Pressão: " << press << " hPa" << std::endl;
        std::cout << "Umidade: " << hum << " %" << std::endl;
        std::cout << "--------------------------" << std::endl;

        sleep(2);
    }
}
