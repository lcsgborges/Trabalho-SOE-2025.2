import time
import smbus2
import bme280

# BM280 sensor address
address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(1)

#Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

while True:
    try:
        data = bme280.sample(bus, address, calibration_params)
        temperature = data.temperature
        pressure = data.pressure
        humidity = data.humidity

        print(f"Temperature: {temperature}")
        print(f"Pressure: {pressure}")
        print(f"Humidity: {humidity}")
        time.sleep(2)

    except KeyboardInterrupt:
        print("Program stopped")
        break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break
