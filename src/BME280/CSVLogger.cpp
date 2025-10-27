#include "CSVLogger.h"
#include <iostream>

CSVLogger::CSVLogger(const std::string& fileName)
    : path(fileName), writtenHeader(false)
{
    file.open(path, std::ios::app);

    if (!file.is_open()) {
        std::cerr << "Erro ao abrir arquivo CSV: " << path << std::endl;
        return;
    }

    // se o arquivo estiver vazio, escreve cabeçaçho
    file.seekp(0, std::ios::end);
    if (file.tellp() == 0) {
        writeHeader("date,time,temperature,pressure,humidity");
    }
}

CSVLogger::~CSVLogger() {
    if (file.is_open()) {
        file.close();
    }
}

void CSVLogger::writeHeader(const std::string& header) {
    if (!file.is_open()) return;

    file << header << "\n";
    file.flush();
    writtenHeader = true;
}

void CSVLogger::writeLine(float temperature, float pressure, float humidity) {
    if (!file.is_open()) return;

    // obtém tempo atual em UTC
    auto now = std::chrono::system_clock::now();
    std::time_t t = std::chrono::system_clock::to_time_t(now);
    std::tm* utc_tm = std::gmtime(&t);

    file << std::put_time(utc_tm, "%d/%m/%Y") << ",";
    file << std::put_time(utc_tm, "%H:%M:%S") << ",";

    file << temperature << "," << pressure << "," << humidity << "\n";

    file.flush();
}