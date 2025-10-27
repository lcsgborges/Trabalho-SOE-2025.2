CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
LDFLAGS = -lwiringPi

SRC = main.cpp SensorBME280.cpp CSVLogger.cpp
OUT = bme280_rpi

all:
	$(CXX) $(CXXFLAGS) $(SRC) -o $(OUT) $(LDFLAGS)

clean:
	rm -f $(OUT)
