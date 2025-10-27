CXX = g++
CXXFLAGS = -std=c++17 -lwiringPi
SRC = main.cpp SensorBME280.cpp
OUT = bme280_rpi

all:
	$(CXX) $(SRC) -o $(OUT) $(CXXFLAGS)

clean:
	rm -f $(OUT)
